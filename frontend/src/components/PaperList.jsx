// import React, { useEffect, useState } from "react";
// import { fetchLLMPapers } from "../api/paperAPI";

// const PaperList = () => {
//   const [papers, setPapers] = useState([]);
//   const [loading, setLoading] = useState(true);

//   const getPapers = async () => {
//     setLoading(true);
//     const result = await fetchLLMPapers();
//     setPapers(result);
//     setLoading(false);
//   };

//   useEffect(() => {
//     getPapers();
//   }, []);

//   return (
//     <div style={styles.wrapper}>
//       <div style={styles.header}>
//         <span style={styles.icon}>📄</span>
//         <h3 style={styles.title}>LLM Papers</h3>
//         <button style={styles.refreshButton} onClick={getPapers}>⟳ Refresh</button>
//       </div>
//       {loading ? (
//         <p style={styles.loading}>Loading papers...</p>
//       ) : (
//         <ul style={styles.paperList}>
//           {papers.map((paper, idx) => (
//             <li key={idx} style={styles.paperItem}>
//               {paper.title || "Untitled"}
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );
// };

// const styles = {
//   wrapper: {
//     backgroundColor: "#fff",
//     padding: "24px",
//     borderRadius: "12px",
//     boxShadow: "0 4px 20px rgba(0, 0, 0, 0.06)",
//     width: "100%",
//     maxWidth: "700px",
//     margin: "40px auto 0",
//     fontFamily: "'Poppins', sans-serif",
//   },
//   header: {
//     display: "flex",
//     alignItems: "center",
//     justifyContent: "space-between",
//     marginBottom: "16px",
//   },
//   icon: {
//     fontSize: "1.5rem",
//     marginRight: "10px",
//   },
//   title: {
//     fontSize: "1.4rem",
//     fontWeight: "600",
//     color: "#1e1e35",
//     margin: 0,
//     flex: 1,
//     textAlign: "left",
//   },
//   refreshButton: {
//     backgroundColor: "#e0e0e0",
//     border: "none",
//     borderRadius: "8px",
//     padding: "8px 16px",
//     cursor: "pointer",
//     fontSize: "0.9rem",
//     fontWeight: 500,
//   },
//   paperList: {
//     listStyle: "none",
//     paddingLeft: "0",
//     marginTop: "10px",
//   },
//   paperItem: {
//     padding: "10px 0",
//     borderBottom: "1px solid #eee",
//     fontSize: "1rem",
//     textAlign: "left",
//   },
//   loading: {
//     fontStyle: "italic",
//     color: "#555",
//     textAlign: "left",
//   },
// };

// export default PaperList;

import React, { useEffect, useState } from "react";
import { fetchLLMPapers } from "../api/paperAPI";

const PaperList = () => {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

  const getPapers = async () => {
    setLoading(true);
    const result = await fetchLLMPapers();

    if (!result || !Array.isArray(result.papers)) {
      console.warn("API returned invalid format:", result);
      setPapers([]);
    } else {
      setPapers(result.papers); // ✅ Use the nested "papers" field
    }

    setLoading(false);
  };

  useEffect(() => {
    getPapers();
  }, []);

  return (
    <div style={styles.wrapper}>
      <div style={styles.header}>
        <span style={styles.icon}>📄</span>
        <h3 style={styles.title}>LLM Papers</h3>
        <button style={styles.refreshButton} onClick={getPapers}>⟳ Refresh</button>
      </div>

      {loading ? (
        <p style={styles.loading}>Loading papers...</p>
      ) : papers.length > 0 ? (
        <div style={styles.tableWrapper}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Title</th>
                <th style={styles.th}>Authors</th>
                <th style={styles.th}>Topic</th>
                <th style={styles.th}>Category</th>
                <th style={styles.th}>Link</th>
              </tr>
            </thead>
            <tbody>
              {papers.map((item, idx) => {
                const paper = item.properties || {};
                return (
                  <tr key={idx} style={styles.tr}>
                    <td style={styles.td}>{paper.title || "Untitled"}</td>
                    <td style={styles.td}>{paper.authors || "—"}</td>
                    <td style={styles.td}>{paper.topic || "—"}</td>
                    <td style={styles.td}>{paper.categories || "—"}</td>
                    <td style={styles.td}>
                      <a
                        href={paper.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.link}
                      >
                        View PDF
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <p style={styles.loading}>No papers found.</p>
      )}
    </div>
  );
};

const styles = {
  wrapper: {
    backgroundColor: "#fff",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.06)",
    width: "100%",
    maxWidth: "1000px",
    margin: "40px auto 0",
    fontFamily: "'Poppins', sans-serif",
    overflowX: "auto",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "20px",
  },
  icon: {
    fontSize: "1.5rem",
    marginRight: "10px",
  },
  title: {
    fontSize: "1.4rem",
    fontWeight: "600",
    color: "#1e1e35",
    margin: 0,
    flex: 1,
    textAlign: "left",
  },
  refreshButton: {
    backgroundColor: "#e0e0e0",
    border: "none",
    borderRadius: "8px",
    padding: "8px 16px",
    cursor: "pointer",
    fontSize: "0.9rem",
    fontWeight: 500,
  },
  tableWrapper: {
    overflowX: "auto",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "0.95rem",
  },
  th: {
    textAlign: "left",
    padding: "10px",
    backgroundColor: "#f5f5f5",
    borderBottom: "2px solid #ddd",
    whiteSpace: "nowrap",
  },
  td: {
    padding: "10px",
    borderBottom: "1px solid #eee",
    verticalAlign: "top",
    whiteSpace: "normal",
  },
  link: {
    color: "#3f3fff",
    textDecoration: "none",
  },
  loading: {
    fontStyle: "italic",
    color: "#555",
    textAlign: "left",
  },
};

export default PaperList;
