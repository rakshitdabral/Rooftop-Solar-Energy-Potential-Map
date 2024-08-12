import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard() {
  const location = useLocation();
  const { lat1, long1, lat2, long2, mapImageUrl } = location.state || {};

  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [efficiency, setEfficiency] = useState(0.18);
  const [solarData, setSolarData] = useState(null);

  useEffect(() => {
    if (lat1 && long1 && lat2 && long2) {
      fetchSolarData(lat1, long1);
    }
  }, [lat1, long1, lat2, long2]);

  const fetchSolarData = async (latitude, longitude) => {
    try {
      const response = await axios.get('https://power.larc.nasa.gov/api/temporal/daily/point', {
        params: {
          parameters: 'ALLSKY_SFC_SW_DWN',
          community: 'RE',
          longitude,
          latitude,
          start: startDate,
          end: endDate,
          format: 'json',
        },
      });
      setSolarData(response.data.properties.parameter.ALLSKY_SFC_SW_DWN);
    } catch (error) {
      console.error('Error fetching solar data:', error);
    }
  };

  const calculateMonthlyAverage = (data) => {
    const monthlyData = {};
    for (const date in data) {
      const month = date.slice(0, 6); // Extract YYYYMM format
      if (!monthlyData[month]) {
        monthlyData[month] = { total: 0, count: 0 };
      }
      monthlyData[month].total += data[date];
      monthlyData[month].count += 1;
    }

    const monthlyAverage = {};
    for (const month in monthlyData) {
      monthlyAverage[month] = monthlyData[month].total / monthlyData[month].count;
    }

    return monthlyAverage;
  };

  const calculateEnergyPotential = (data, area, efficiency) => {
    const energyPotential = {};
    for (const date in data) {
      const month = date.slice(0, 6); // Extract YYYYMM format
      if (!energyPotential[month]) {
        energyPotential[month] = 0;
      }
      energyPotential[month] += data[date] * area * efficiency;
    }

    return energyPotential;
  };

  const monthlyAverage = solarData ? calculateMonthlyAverage(solarData) : {};
  const energyPotential = solarData ? calculateEnergyPotential(solarData, 500, efficiency) : {};

  const solarRadianceData = {
    labels: Object.keys(monthlyAverage),
    datasets: [
      {
        label: 'Monthly Average Solar Radiance (W/m²)',
        data: Object.values(monthlyAverage),
        backgroundColor: 'rgba(13, 136, 230, 0.5)',
      },
    ],
  };

  const energyPotentialData = {
    labels: Object.keys(energyPotential),
    datasets: [
      {
        label: 'Monthly Solar Energy Potential (Wh)',
        data: Object.values(energyPotential),
        backgroundColor: 'rgba(255, 187, 51, 0.5)',
      },
    ],
  };

  const annualEnergyPotential = Object.values(energyPotential).reduce((acc, val) => acc + val, 0);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold text-center text-white font-mono mb-4">Solar Potential Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl text-white font-semibold text-center mb-2">Monthly Average Solar Radiance</h2>
          <Bar data={solarRadianceData} />
        </div>
        <div>
          <h2 className="text-xl text-white font-semibold text-center mb-2">Monthly Solar Energy Potential</h2>
          <Bar data={energyPotentialData} />
        </div>
      </div>

      <div className="mt-4">
        <h2 className="text-xl text-white font-semibold text-center">Annual Solar Energy Potential (Wh)</h2>
        <p className="text-center text-white text-2xl font-bold">{annualEnergyPotential.toFixed(2)}</p>
      </div>

      {mapImageUrl && (
        <div className="mt-4 flex justify-center">
          <img src={mapImageUrl} alt="Saved Satellite Image" className="border border-gray-300 rounded shadow-lg" />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
