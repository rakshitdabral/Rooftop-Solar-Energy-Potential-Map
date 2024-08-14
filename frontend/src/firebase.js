
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCh3aFIfk-zO7VX6z6Cx6qSbAyF6rsY9ss",
  authDomain: "authentication-6b640.firebaseapp.com",
  projectId: "authentication-6b640",
  storageBucket: "authentication-6b640.appspot.com",
  messagingSenderId: "380019441796",
  appId: "1:380019441796:web:97881526634790ce5b02d1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth,GoogleAuthProvider };


