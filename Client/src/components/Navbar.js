import React from 'react';
import { Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import logo from '../assests/logo.png'

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
  return (
    <div className='flex justify-between items-center p-4  text-white '>
      {/* Logo Section */}
      <div className="flex items-center">
        <div className="h-10 mr-4">
          </div>
          <span>
            <img src={logo} width= "120px" height= "130px" />
          </span>
        <span className="text-xl font-bold"></span>
      </div>

      <nav className='flex-grow font-mono'>
  <ul className='flex justify-center gap-4'>
    <li>
      <Link
        to="/"
        className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600"
      >
        Home
      </Link>
    </li>
    <li>
      <Link
        to="/"
        className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600"
      >
        About us
      </Link>
    </li>
    <li>
      <Link
        to="/"
        className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600"
      >
        Contact
      </Link>
    </li>
  </ul>
</nav>

      
      <div className='flex gap-x-3 font-mono'>
        {!isLoggedIn &&
          <>
            <Link to="/login">
              <button className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600">
                Login
              </button>
            </Link>
            <Link to="/signup">
              <button className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600">
                Sign up
              </button>
            </Link>
          </>
        }
        {isLoggedIn &&
          <>
            <button onClick={() => { setIsLoggedIn(false); toast.success("Logged out"); }}
            className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600">
              Log out
            </button>
            <Link to="/dashboard">
              <button className="px-4 py-2 text-white text-2xl rounded-md shadow-md font-normal border-b-2 border-transparent hover:border-blue-600">
                Dashboard
              </button>
            </Link>
          </>
        }
      </div>
      <ToastContainer />
    </div>
  );
}