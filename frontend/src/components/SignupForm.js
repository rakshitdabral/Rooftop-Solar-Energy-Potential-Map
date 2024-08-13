import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import { auth, GoogleAuthProvider } from '../firebase';
import { createUserWithEmailAndPassword, signInWithPopup } from 'firebase/auth';

const SignupForm = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();
  const [userdata, setUserData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    setpassword: "",
    confirmpassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});

  const changeHandler = (event) => {
    const { name, value } = event.target;
    setUserData({ ...userdata, [name]: value });
    // Clear validation errors on change
    setErrors({ ...errors, [name]: "" });
  };

  const validateForm = () => {
    const newErrors = {};

    // Validate email
    if (!userdata.email.trim()) {
      newErrors.email = "Please enter an email";
    } else if (!userdata.email.includes("@") || !userdata.email.includes(".")) {
      newErrors.email = "Invalid email format";
    }

    // Validate password
    if (!userdata.setpassword.trim()) {
      newErrors.setpassword = "Please enter a password";
    } else if (userdata.setpassword.length < 8) {
      newErrors.setpassword = "Password should be at least 8 characters long";
    }

    // Validate confirm password
    if (!userdata.confirmpassword.trim()) {
      newErrors.confirmpassword = "Please confirm your password";
    } else if (userdata.setpassword !== userdata.confirmpassword) {
      newErrors.confirmpassword = "Passwords do not match";
    }

    setErrors(newErrors);

    // Return true if there are no errors
    return Object.keys(newErrors).length === 0;
  };

  const submitHandler = async (event) => {
    event.preventDefault();
    if (validateForm()) {
      try {
        await createUserWithEmailAndPassword(auth, userdata.email, userdata.setpassword);
        setIsLoggedIn(true);
        toast.success("Account created successfully");
        navigate("/dashboard");
      } catch (error) {
        toast.error(error.message);
      }
    }
  };

  const handleGoogleSignIn = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      setIsLoggedIn(true);
      toast.success("Signed in with Google successfully");
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div>
      <form onSubmit={submitHandler} className="space-y-4">
        <div className="flex space-x-4">
          <label className="w-1/2 block">
            <p className='text-white text-xl font-bold'>First name <sup>*</sup></p>
            <input
              type="text"
              placeholder="Enter your first name"
              onChange={changeHandler}
              name="firstname"
              value={userdata.firstname}
              className="w-full px-3 py-2 border rounded"
            />
            {errors.firstname && <p className="text-red-500 text-sm">{errors.firstname}</p>}
          </label>
          <label className="w-1/2 block">
            <p className='text-white text-xl '>Last name <sup>*</sup></p>
            <input
              type="text"
              placeholder="Enter your last name"
              onChange={changeHandler}
              name="lastname"
              value={userdata.lastname}
              className="w-full px-3 py-2 border rounded"
            />
            {errors.lastname && <p className="text-red-500 text-sm">{errors.lastname}</p>}
          </label>
        </div>
        <label className="block">
          <p className='text-white text-xl '>Email Address <sup>*</sup></p>
          <input
            type="email"
            placeholder="Enter your email"
            onChange={changeHandler}
            name="email"
            value={userdata.email}
            className="w-full px-3 py-2 border rounded"
          />
          {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}
        </label>
        <div className="flex space-x-4">
          <label className="w-1/2 block">
            <p className='text-white text-xl '>Set Password <sup>*</sup></p>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter password"
                onChange={changeHandler}
                name="setpassword"
                value={userdata.setpassword}
                className="w-full px-2 py-2 border rounded"
              />
              <span
                onClick={() => setShowPassword((prev) => !prev)}
                className="absolute right-3 top-3 cursor-pointer"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
              </span>
            </div>
            {errors.setpassword && <p className="text-red-500 text-sm">{errors.setpassword}</p>}
          </label>
          <label className="w-1/2 block">
            <p className='text-white text-xl'>Confirm Password <sup>*</sup></p>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Confirm password"
                onChange={changeHandler}
                name="confirmpassword"
                value={userdata.confirmpassword}
                className="w-full px-3 py-2 border rounded"
              />
              <span
                onClick={() => setShowPassword((prev) => !prev)}
                className="absolute right-3 top-3 cursor-pointer"
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
              </span>
            </div>
            {errors.confirmpassword && <p className="text-red-500 text-sm">{errors.confirmpassword}</p>}
          </label>
        </div>
        <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
          Create Account
        </button>
      </form>
      <div className="text-center my-4 text-2xl font-bold text-white">OR</div>
      <div className="mt-4">
        <button
          onClick={handleGoogleSignIn}
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600 flex items-center justify-center space-x-2"
        >
          <span>Sign Up with Google</span>
        </button>
      </div>

      <ToastContainer />
    </div>
  );
};

export default SignupForm;