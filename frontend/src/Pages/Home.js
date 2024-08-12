import React, { useState, useRef } from 'react';
import { GoogleMap, LoadScript, Polygon } from '@react-google-maps/api';
import p1 from '../assests/p1.png';
import solar from '../assests/solar.png';
import { FaLinkedin, FaInstagram, FaGithub } from 'react-icons/fa';

const Home = () => {
  const [map, setMap] = useState(null);
  const [polygon, setPolygon] = useState(null);
  const [lat1, setLat1] = useState('');
  const [long1, setLong1] = useState('');
  const [lat2, setLat2] = useState('');
  const [long2, setLong2] = useState('');
  const [mapImageUrl, setMapImageUrl] = useState('');
  const mapRef = useRef(null);

  const defaultCenter = { lat: 22.5726, lng: 88.3639 };

  const handleMapLoad = (mapInstance) => {
    setMap(mapInstance);
  };

  const handleInputChange = (e, setter) => {
    setter(e.target.value);
  };

  const validateCoordinates = () => {
    const latDiff = Math.abs(parseFloat(lat1) - parseFloat(lat2));
    const lngDiff = Math.abs(parseFloat(long1) - parseFloat(long2));
    
    return latDiff <= 0.0002 && lngDiff <= 0.0002;
  };

  const createPolygon = () => {
    const coordsArray = [
      { lat: parseFloat(lat1), lng: parseFloat(long1) },
      { lat: parseFloat(lat2), lng: parseFloat(long2) }
    ];

    if (!validateCoordinates()) {
      alert('Latitude and longitude differences must not be greater than 0.0002.');
      return;
    }

    setPolygon(coordsArray);
    fitMapToPolygon(coordsArray);
  };

  const fitMapToPolygon = (coordsArray) => {
    if (map) {
      const bounds = new window.google.maps.LatLngBounds();
      coordsArray.forEach((coord) => bounds.extend(new window.google.maps.LatLng(coord.lat, coord.lng)));
      map.fitBounds(bounds);
    }
  };

  const saveImage = () => {
    if (polygon && polygon.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      polygon.forEach((coord) => bounds.extend(new window.google.maps.LatLng(coord.lat, coord.lng)));
      const center = bounds.getCenter();
      const zoom = map.getZoom();
      const staticMapUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${center.lat()},${center.lng()}&zoom=${zoom}&size=600x400&maptype=satellite&key=AIzaSyB4mze3dCYLlVzGEWO-cyHZYEiV01JD6iM`;
      setMapImageUrl(staticMapUrl);

      // Display the image on the homepage
      document.getElementById('mapImage').innerHTML = ''; // Clear previous image
      const imgElement = document.createElement('img');
      imgElement.src = staticMapUrl;
      imgElement.alt = 'Satellite Image';
      document.getElementById('mapImage').appendChild(imgElement);
    }
  };

  return (
    <>
      <div className='flex'>
        <div>
          <img src={p1} width="700px" height="700px" className='p-20' />
          <div className='text-white text-3xl leading-10 border-l-8 space-x-5 font-mono ml-16 border-blue-600'>
            <p className='space-x-5'>ANY QUERIES? VISIT US</p>
            <a href='https://isro.hack2skill.com/2024/'>isro.hack2skill.com</a> <br/>
          </div>
          <div className="flex space-x-6 mt-2 ml-16">
            <a
              href="https://www.linkedin.com/in/yash-pandey"
              className="text-blue-500 hover:text-blue-700 text-2xl"
            >
              <FaLinkedin />
            </a>
            <a
              href="https://www.instagram.com/shibu___16"
              className="text-pink-500 hover:text-pink-700 text-2xl"
            >
              <FaInstagram />
            </a>
            <a
              href="https://github.com/Yash16p"
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              <FaGithub />
            </a>
          </div>
        </div>
        <div>
          <img src={solar} width="700px" height="700px" className='p-20 animate-horizontal-move' />
        </div>
      </div>

      <div className="h-screen flex flex-col items-center justify-center">
        <div className="w-full max-w-3xl p-4">
          <h1 className="font-bold text-3xl mb-2 text-center text-white font-mono">Select Area</h1>
          <h3 className="text-xl mb-3 text-center text-white font-mono">
            Select an Area on the map to estimate the solar energy potential for rooftops.
          </h3>
          <LoadScript googleMapsApiKey="AIzaSyB4mze3dCYLlVzGEWO-cyHZYEiV01JD6iM">
            <div className="flex justify-center p-6">
              <GoogleMap
                mapContainerStyle={{ height: '40vh', width: '100%' }}
                center={defaultCenter}
                zoom={10}
                onLoad={handleMapLoad}
              >
                {polygon && (
                  <Polygon
                    paths={polygon}
                    options={{
                      strokeColor: '#FF0000',
                      strokeOpacity: 0.8,
                      strokeWeight: 2,
                      fillColor: '#FF0000',
                      fillOpacity: 0.35,
                    }}
                  />
                )}
              </GoogleMap>
            </div>
          </LoadScript>
        </div>
        <div className="p-8 w-full max-w-3xl mt-4">
          <div className="flex flex-col items-center space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <input
                  type="text"
                  value={lat1}
                  onChange={(e) => handleInputChange(e, setLat1)}
                  placeholder="Latitude 1"
                  className="p-2 border border-gray-300 text-white text-xl rounded w-full bg-black font-mono"
                />
                <input
                  type="text"
                  value={long1}
                  onChange={(e) => handleInputChange(e, setLong1)}
                  placeholder="Longitude 1"
                  className="p-2 border border-gray-300 rounded w-full mt-2 text-white text-xl bg-black font-mono"
                />
              </div>
              <div>
                <input
                  type="text"
                  value={lat2}
                  onChange={(e) => handleInputChange(e, setLat2)}
                  placeholder="Latitude 2"
                  className="p-2 border border-gray-300 rounded w-full text-white text-xl bg-black font-mono"
                />
                <input
                  type="text"
                  value={long2}
                  onChange={(e) => handleInputChange(e, setLong2)}
                  placeholder="Longitude 2"
                  className="p-2 border border-gray-300 rounded w-full mt-2 text-white text-xl bg-black font-mono"
                />
              </div>
            </div>

            <div className="flex space-x-4 top-10 w-full justify-center">
              <button
                onClick={createPolygon}
                className="p-4 bg-gray-900 text-2xl w-2/3 text-white rounded-xl font-mono hover:bg-gray-700"
              >
                Submit
              </button>

              <button
                onClick={saveImage}
                className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-700"
              >
                Save Satellite Image
              </button>
            </div>
          </div>
          <div id="mapImage" className="p-4 mt-4"></div>
        </div>
      </div>
      <style jsx="true">{`
        @keyframes moveHorizontally {
          0% { transform: translateX(0); }
          50% { transform: translateX(70px); }
          100% { transform: translateX(100px); }
        }

        .animate-horizontal-move {
          animation: moveHorizontally 4s infinite alternate;
        }
      `}</style>
    </>
  );
};

export default Home;
