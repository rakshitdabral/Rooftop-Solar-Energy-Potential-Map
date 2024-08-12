import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../firebase';

export default function LoginForm({ setIsLoggedIn }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);

  function changeHandler(event) {
    setFormData((prevData) => ({
      ...prevData,
      [event.target.name]: event.target.value,
    }));
  }

  async function submitHandler(event) {
    event.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, formData.email, formData.password);
      setIsLoggedIn(true);
      toast.success("Logged in successfully");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Login failed: " + error.message);
    }
  }

  async function handleGoogleSignIn() {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
      setIsLoggedIn(true);
      toast.success("Logged in with Google");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Google Sign-In failed: " + error.message);
    }
  }

  return (
    <div>
      <form onSubmit={submitHandler} className="space-y-4">
        <label className="block">
          <p className='text-white text-xl'>Email Address <sup>*</sup></p>
          <input
            required
            type='email'
            onChange={changeHandler}
            placeholder='Enter your email'
            value={formData.email}
            name='email'
            className="w-full px-3 py-2 border rounded"
          />
        </label>
        <label className="block">
          <p className='text-white text-xl'>Password <sup>*</sup></p>
          <div className="relative">
            <input
              required
              type={showPassword ? "text" : "password"}
              onChange={changeHandler}
              placeholder='Enter your password'
              value={formData.password}
              name='password'
              className="w-full px-3 py-2 border rounded"
            />
            <span
              onClick={() => setShowPassword((prev) => !prev)}
              className="absolute right-3 top-3 cursor-pointer"
            >
              {showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
            </span>
          </div>
        </label>
        <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
          Log in
        </button>
        <div className="text-center my-4 text-2xl font-bold text-white">OR</div>
        <button
          type="button"
          onClick={handleGoogleSignIn}
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600 mt-4"
        >
          Log in with Google
        </button>
      </form>
      <ToastContainer />
    </div>
  );
}
