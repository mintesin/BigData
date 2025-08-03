import React, { useState, useEffect } from "react";
import { API } from "./api.jsx"; // Adjust the path as needed

export function PartTwo() {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await API.parttwo(); // assuming this returns JSON
        setData(response.data); // if using axios, use `.data`
        console.log("Data retrieved successfully");
      } catch (error) {
        console.log("The data is not being retrieved correctly", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h3>Part Two Data</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
