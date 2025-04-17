import React from 'react';
import { FaDownload } from "react-icons/fa6";

export const DownloadCard = ({ category, feedImageUrl, storiesImageUrl }) => {
  return (
    <div className="card card-animated">
      <div className="card-header">{category}</div>
      <div className="card-body px-2 py-2">
        <a
          href={feedImageUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-outline-custom d-flex align-items-center mb-2"
        >
          <FaDownload className="me-2" /> Feed
        </a>
        <a
          href={storiesImageUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-outline-custom d-flex align-items-center"
        >
          <FaDownload className="me-2" /> Stories
        </a>
      </div>
    </div>
  );
};
