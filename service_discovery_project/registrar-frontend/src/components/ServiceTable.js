import { useState, useEffect } from "react";
import './ServiceTable.css';  // Import the CSS file

const ServiceTable = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch services from the FastAPI backend
  const fetchServices = async () => {
    setLoading(true);
    try {
      // Make a GET request to the FastAPI '/services' endpoint
      const response = await fetch("http://localhost:8000/services"); // FastAPI backend URL
      if (!response.ok) throw new Error("Failed to fetch services");
      
      const data = await response.json();
      setServices(data);
    } catch (error) {
      console.error("Error fetching services:", error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch services when the component mounts
  useEffect(() => {
    fetchServices();
  }, []);

  return (
    <div className="service-table-container">
      <h1 className="title">Available Services</h1>

      <button
        onClick={fetchServices}
        className="refresh-button"
        disabled={loading}
      >
        {loading ? "Refreshing..." : "Refresh List"}
      </button>

      <table className="service-table">
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Address</th>
            
          </tr>
        </thead>
        <tbody>
          {services.length > 0 ? (
            services.map((service, index) => (
              <tr key={index}>
                <td>{service.name}</td>
                <td>{service.address}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" className="no-services">
                No services available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ServiceTable;
