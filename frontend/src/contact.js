import "./contact.css";

export default function ContactCard() {
  return (
    <div className="contact-card">
      <h1 className="contact-title">Contact Us</h1>
      <p className="contact-info">
        Agence Nationale de l’Aviation Civile du Togo<br />
        Adresse : B.P. 2699, Lomé - TOGO<br />
        Tél : +228 22263740<br />
        Fax : +228 22260860<br />
        Site Web : <a href="http://www.anac-togo.tg">www.anac-togo.tg</a><br />
        E-mail 1: <a href="mailto:secretariat@anac-togo.tg">secretariat@anac-togo.tg</a><br />
        E-mail 2: <a href="mailto:anactogo@gmail.com">anactogo@gmail.com</a><br />
        E-mail 3: <a href="mailto:anac@anac-togo.tg">anac@anac-togo.tg</a>
      </p>
    </div>
  );
}

