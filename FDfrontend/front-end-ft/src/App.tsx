import React, { useState } from "react";
import axios from "axios";
import { useForm, SubmitHandler } from "react-hook-form";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

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
    formState: { isValid },
  } = useForm<Location>();

  const fetchTrucks = async (data: Location, nextPage: number = 1) => {
    try {
      console.log(data);
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
            step="any"
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
            step="any"
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
            step="any"
            className="form-control"
            id="radius"
          />
        </div>
        <button type="submit" disabled={!isValid} className="btn btn-primary">
          Submit
        </button>
      </form>

      <h1>Trucks</h1>
      <div className="tableDiv">
        <table className="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">NAME</th>
              <th scope="col">TYPE</th>
              <th scope="col">STATUS</th>
            </tr>
          </thead>
          <tbody>
            {trucks.map((truck, index) => (
              <tr>
                <th scope="row">{index + 1}</th>
                <td>{truck.fields.name}</td>
                <td>{truck.fields.type}</td>
                <td>{truck.fields.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <button
          onClick={handlePreviousPage}
          className="buttonMove"
          disabled={page === 1}
        >
          Previous Page
        </button>
        <span>Page {page}</span>
        <button onClick={handleNextPage} className="buttonMove">
          Next Page
        </button>
      </div>
    </>
  );
};

export default App;
