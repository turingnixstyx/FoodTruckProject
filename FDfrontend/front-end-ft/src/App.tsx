import React, { useState } from "react";
import axios from "axios";
import { useForm, SubmitHandler } from "react-hook-form";
import "bootstrap/dist/css/bootstrap.min.css";

interface Location {
  x: number;
  y: number;
  radius: number;
}

interface Truck {
  model: string;
  pk: number;
  fields: {
    name: string;
    type: string;
    locationx: string;
    locationy: string;
    status: string;
    rel_distance: string;
  };
}

interface TrucksResponse {
  trucks: Truck[];
  has_next: boolean;
  has_previous: boolean;
  total_pages: number;
  current_page: number;
}

const App: React.FC = () => {
  const [trucks, setTrucks] = useState<Truck[]>([]);
  const [page, setPage] = useState<number>(1);
  const [location, setLocation] = useState<Location>({
    x: -1,
    y: -1,
    radius: 0,
  });
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<Location>();

  const fetchTrucks = async (data: Location, nextPage: number = 1) => {
    try {
      const response = await axios.post<TrucksResponse>(
        `http://localhost:8000/location/?page=${nextPage}`,
        data
      );

      const newTrucks = JSON.parse(response.data.trucks);
      setTrucks(newTrucks);
      setPage(response.data.current_page);
    } catch (error) {
      console.error("Error fetching trucks:", error);
    }
  };

  const handleFormData: SubmitHandler<Location> = (data) => {
    setLocation(data);
    fetchTrucks(data);
  };

  const handleNextPage = () => {
    const nextPage = page + 1;
    fetchTrucks(location, nextPage);
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      const previousPage = page - 1;
      fetchTrucks(location, previousPage);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit(handleFormData)}>
        <div className="mb-3">
          <label htmlFor="XCord" className="form-label">
            Location X
          </label>
          <input
            {...register("x", { required: true })}
            type="number"
            className="form-control"
            id="XCord"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="YCord" className="form-label">
            Location Y
          </label>
          <input
            {...register("y", { required: true })}
            type="number"
            className="form-control"
            id="YCord"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="radius" className="form-label">
            Radius
          </label>
          <input
            {...register("radius")}
            type="number"
            className="form-control"
            id="radius"
          />
        </div>
        <button type="submit" disabled={!isValid} className="btn btn-primary">
          Submit
        </button>
      </form>

      <h1>Trucks</h1>
      <ul>
        {trucks.map((truck) => (
          <li key={truck.pk}>
            <h2>{truck.fields.name}</h2>
            <p>Type: {truck.fields.type}</p>
            <p>Status: {truck.fields.status}</p>
            <p>Relative Distance: {truck.fields.rel_distance}</p>
          </li>
        ))}
      </ul>

      <table className="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">First</th>
            <th scope="col">Last</th>
            <th scope="col">Handle</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1</th>
            <td>Mark</td>
            <td>Otto</td>
            <td>@mdo</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>Jacob</td>
            <td>Thornton</td>
            <td>@fat</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td colSpan="2">Larry the Bird</td>
            <td>@twitter</td>
          </tr>
        </tbody>
      </table>

      <div>
        <button onClick={handlePreviousPage} disabled={page === 1}>
          Previous Page
        </button>
        <span>Page {page}</span>
        <button onClick={handleNextPage}>Next Page</button>
      </div>
    </>
  );
};

export default App;
