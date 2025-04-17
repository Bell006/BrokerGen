import React from 'react';

export const CategoryBtn = ({ id, value, checked, onChange, label }) => {
  return (
    <div className="col-6 col-md-4 mb-2">
      <div className="form-check">
        <input
          type="checkbox"
          className="form-check-input"
          id={id}
          value={value}
          checked={checked}
          onChange={onChange}
        />
        <label className="form-check-label" htmlFor={id}>
          {label}
        </label>
      </div>
    </div>
  );
};