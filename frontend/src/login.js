import React from "react";
import "./login.css";

export function Login({ goSignup }) {
  return (
    <div className="BoxLog">
      <h2 className="Login">Login</h2>

      <form className="formulare">
        <input type="email" className="require" placeholder="Adresse email" />
        <input type="password" className="require" placeholder="Mot de passe" />
        <button className="submit_button">
          Submit
        </button>
      </form>

      <p className="question">
        Don't have an account?{' '}
        <button onClick={goSignup} className="text-blue-600 font-semibold">
          Sign up
        </button>
      </p>
    </div>
  );
}
