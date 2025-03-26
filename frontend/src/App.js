// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


// import React from "react";
// import "./App.css";
// import logo from "./Pitchdeck - daimon.AI .png"; // Make sure the file is in src/

// function App() {
//   return (
//     <div style={styles.container}>
//       <img src={logo} alt="Daimon Logo" style={styles.logo} />
//       <div style={styles.sloganBlock}>
//         <h1 style={styles.sloganBold}>your trusted compass</h1>
//         <h2 style={styles.sloganLight}>in the LLM research landscape</h2>
//       </div>
//       <div style={styles.searchWrapper}>
//         <span style={styles.searchIcon}>🔍</span>
//         <input
//           type="text"
//           placeholder="Search..."
//           style={styles.searchbar}
//         />
//       </div>
//     </div>
//   );
// }

// const styles = {
//   container: {
//     backgroundColor: "#f5f6fa",
//     height: "100vh",
//     display: "flex",
//     flexDirection: "column",
//     justifyContent: "center",
//     alignItems: "center",
//     textAlign: "center",
//     padding: "0 20px",
//     fontFamily: "'Poppins', sans-serif",
//   },
//   logo: {
//     height: "230px",
//     marginBottom: "20px",
//     transition: "transform 0.3s ease",
//   },
//   sloganBlock: {
//     marginBottom: "35px",
//     animation: "fadeIn 1.2s ease-out",
//   },
//   sloganBold: {
//     fontSize: "2.4rem",
//     fontWeight: 700,
//     color: "#1e1e35",
//     margin: 0,
//   },
//   sloganLight: {
//     fontSize: "2.2rem",
//     fontWeight: 400,
//     color: "#1e1e35",
//     marginTop: "5px",
//   },
//   searchWrapper: {
//     position: "relative",
//     width: "360px",
//     maxWidth: "90%",
//   },
//   searchIcon: {
//     position: "absolute",
//     left: "14px",
//     top: "50%",
//     transform: "translateY(-50%)",
//     fontSize: "1.1rem",
//     color: "#888",
//   },
//   searchbar: {
//     padding: "14px 24px 14px 40px",
//     fontSize: "1rem",
//     borderRadius: "12px",
//     border: "1px solid #ddd",
//     outline: "none",
//     width: "100%",
//     backgroundColor: "#fff",
//     boxShadow: "0 4px 18px rgba(0, 0, 0, 0.08)",
//   },
// };

// export default App;


import React from "react";
import "./App.css";
import logo from "./Pitchdeck - daimon.AI .png"; // Make sure this file is in src/
import PaperList from "./components/PaperList"; // Import the paper list

function App() {
  return (
    <div style={styles.container}>
      <img src={logo} alt="Daimon Logo" style={styles.logo} />

      <div style={styles.sloganBlock}>
        <h1 style={styles.sloganBold}>your trusted compass</h1>
        <h2 style={styles.sloganLight}>in the LLM research landscape</h2>
      </div>

      <div style={styles.searchWrapper}>
        <span style={styles.searchIcon}>🔍</span>
        <input
          type="text"
          placeholder="Search..."
          style={styles.searchbar}
        />
      </div>

      {/* 🔽 Paper list section */}
      <div style={styles.paperListWrapper}>
        <PaperList />
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#f5f6fa",
    minHeight: "100vh",
    padding: "40px 20px",
    fontFamily: "'Poppins', sans-serif",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  logo: {
    height: "230px",
    marginBottom: "20px",
    transition: "transform 0.3s ease",
  },
  sloganBlock: {
    marginBottom: "35px",
    animation: "fadeIn 1.2s ease-out",
    textAlign: "center",
  },
  sloganBold: {
    fontSize: "2.4rem",
    fontWeight: 700,
    color: "#1e1e35",
    margin: 0,
  },
  sloganLight: {
    fontSize: "2.2rem",
    fontWeight: 400,
    color: "#1e1e35",
    marginTop: "5px",
  },
  searchWrapper: {
    position: "relative",
    width: "360px",
    maxWidth: "90%",
    marginBottom: "50px",
  },
  searchIcon: {
    position: "absolute",
    left: "14px",
    top: "50%",
    transform: "translateY(-50%)",
    fontSize: "1.1rem",
    color: "#888",
  },
  searchbar: {
    padding: "14px 24px 14px 40px",
    fontSize: "1rem",
    borderRadius: "12px",
    border: "1px solid #ddd",
    outline: "none",
    width: "100%",
    backgroundColor: "#fff",
    boxShadow: "0 4px 18px rgba(0, 0, 0, 0.08)",
  },
  paperListWrapper: {
    marginTop: "20px",
    width: "100%",
    maxWidth: "800px",
  },
};

export default App;
