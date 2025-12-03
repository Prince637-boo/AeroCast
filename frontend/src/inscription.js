import React from 'react';
import './inscription.css';

export function Signup({ goLogin }) {
  return (
    <div className="BoxSign">
      <h2 className="Sign">Sign Up</h2>

      <form className="formulare">
        <input className="require" placeholder="Nom" />
        <input className="require" placeholder="Prénom" />
        <input type="email" className="require" placeholder="Adresse email" />     
        <input type="text" className="require" placeholder="Numéro de passeport" />
        <input type="date" className="require" placeholder="Date de naissance" />
        <input type="password" className="require" placeholder="Mot de passe" />
        <input type="password" className="require" placeholder="Confirmer le mot de passe" />
        <button className="submit_button">
          Submit
        </button>
      </form>

      <p className="quetion">
        You already have an account?{' '}
        <button onClick={goLogin} className="text-blue-600 font-semibold">
          Login
        </button>
      </p>
    </div>
  );
}
