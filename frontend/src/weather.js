import { useState, useEffect } from "react";
import "./weather.css";

export default function Weather() {
  const [time, setTime] = useState(new Date());
  const [city, setCity] = useState("");
  const [weatherData, setWeatherData] = useState(null);

  // Horloge
  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const hours = time.getHours();
  const minutes = time.getMinutes();
  const displayHour = hours % 12 || 12;
  const ampm = hours >= 12 ? "PM" : "AM";
  const formattedMinutes = minutes < 10 ? "0" + minutes : minutes;

  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];

  const dayName = days[time.getDay()];
  const dayNumber = time.getDate();
  const monthName = months[time.getMonth()];

  // Recherche
  const handleSearch = (e) => {
    e.preventDefault();

    const fakeData = {
      temp: 32,
      realFeel: 39,
      realFeelShade: 36,
      wind: "S 20 km/h",
      gusts: "20 km/h",
      airQuality: "Correct",
      description: "Partiellement ensoleillé",
    };

    setWeatherData(fakeData);
  };


  return (
    <div className="weather-container">

      <div className="card">
        <p className="day-text">{dayName}, {monthName} {dayNumber}</p>
        <p className="time-text">
          {displayHour}:{formattedMinutes}
          <span className="time-sub-text">{ampm}</span>
        </p>
      </div>

      <form className="weather-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Entrez votre ville..."
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button type="submit">Rechercher</button>
      </form>

      {weatherData && (
        <div className="weather-card">

          <div className="weather-left">
            <img src="/weather-icons/sun-cloud.png" alt="icon" className="weather-icon" />

            <div>
              <div className="temp">{weatherData.temp}°</div>
              <div className="realfeel">RealFeel {weatherData.realFeel}°</div>
              <div className="desc">{weatherData.description}</div>
            </div>
          </div>

          <div className="weather-right">
            <div className="row"><span>RealFeel Shade</span> <b>{weatherData.realFeelShade}°</b></div>
            <div className="row"><span>Vent</span> <b>{weatherData.wind}</b></div>
            <div className="row"><span>Rafales</span> <b>{weatherData.gusts}</b></div>
            <div className="row"><span>Qualité de l'air</span> <b className="good">{weatherData.airQuality}</b></div>
          </div>

        </div>
      )}

    </div>
  );
}
