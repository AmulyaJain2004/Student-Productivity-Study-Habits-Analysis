import { useState } from "react";
import { getPrediction } from "./services/api";

function App() {
  const [inputValue, setInputValue] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handlePredict = async () => {
    const result = await getPrediction(Number(inputValue));
    setPrediction(result);
  };

  return (
    <div>
      <h1>React + Django ML Prediction</h1>
      <input
        type="number"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Enter a number"
      />
      <button onClick={handlePredict}>Predict</button>
      {prediction !== null && <p>Prediction: {prediction}</p>}
    </div>
  );
}

export default App;
