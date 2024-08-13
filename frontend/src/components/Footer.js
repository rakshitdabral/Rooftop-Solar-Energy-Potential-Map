import React from 'react'
import logo from '../assests/logo.png'
import { FaLinkedin, FaInstagram, FaGithub } from 'react-icons/fa';

function Footer() {

  return (
    <div className=''>
      <div className='border-t-2 p-5 mb-12 flex justify-around items-center mt-6'>
        <div>
          <img src={logo} width="200px" height="200px" />
        </div>

        <div>
          <h2 className='text-white font-bold text-2xl mb-2'>Useful Links</h2>
          <ul className='text-white leading-10'>
            <li>Our Projects</li>
            <li>FAQ's</li>
            <li>News and updates</li>
          </ul>
        </div>

        <div>
          <h2 className='text-white font-bold text-2xl mb-2'>Quick Links</h2>
          <ul className='text-white leading-10'>
            <li>Privacy Policy</li>
            <li>Terms of Service</li>
            <li>Careers</li>
            <li>Blog</li>
          </ul>
        </div>

        <div>
          <h2 className='text-white font-bold text-2xl mb-2'>Contacts</h2>
          <ul className='text-white leading-10'>
            <li>Our Projects</li>
            <li>FAQ's</li>
            <li>News and updates</li>
          </ul>
        </div>
      </div>

      <div className='flex flex-col items-center p-8'>
        <h2 className='text-white text-2xl mb-4'>Follow us</h2>
        <div className="flex space-x-4 mt-2">
          <a
            href="https://www.linkedin.com/in/yash-pandey"
            className="text-blue-500 hover:text-blue-700 text-2xl"
          >
            <FaLinkedin />
          </a>
          <a
            href="https://www.instagram.com/shibu___16"
            className="text-pink-500 hover:text-pink-700  text-2xl"
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

      <div className='flex justify-center mt-4'>
        <p className='font-mono text-white mb-5'>All Copywrites Reserved</p>
      </div>
    </div>
  )
}

export default Footer