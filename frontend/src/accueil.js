import { useState } from "react";
import { Signup } from "./inscription";
import { Login } from "./login";
import WeatherCard from "./weather";
import ContactCard from "./contact";
import "./accueil.css";

export default function Accueil() {
  const [page, setPage] = useState("home");

  return (
    <div className="Home">
      <nav className="navbar">
        <div className="nav-left">
          <button onClick={() => setPage("home")} className="nav-btn">Home</button>
          <button onClick={() => setPage("weather")} className="nav-btn">Weather</button>
          <button onClick={() => setPage("contact")} className="nav-btn">Contact Us</button>
        </div>

        <div className="nav-right">
          <button onClick={() => setPage("login")} className="nav-btn login-btn">Login</button>
          <button onClick={() => setPage("signup")} className="nav-btn signup-btn">Sign Up</button>
        </div>
      </nav>

      <div className="content">
        {page === "home" && <Home />}
        {page === "login" && <Login goSignup={() => setPage("signup")} />}
        {page === "signup" && <Signup goLogin={() => setPage("login")} />}
        {page === "weather" && <WeatherCard />}
        {page === "contact" && <ContactCard />}
      </div>

      <footer className="footer">
        <p>© 2025 AMP. Tous droits réservés.</p>
      </footer>
    </div>
  );
}


function Home() {
  return (
    <div className="page-card">
      <h1 className="text-3xl font-bold mb-6">Bienvenue</h1>
      <p>Bienvenue sur notre site de prévision météo !<br />Découvrez les dernières prévisions et restez informé.</p>
    </div>
  );
}



 
