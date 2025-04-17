import React from 'react';
import InputMask from "react-input-mask";


export const Input = ({ label, type, name, value, onChange, placeholder, required, mask }) => {

    let digit = /[0-9]/;
    let mobileMask = ['(', digit, digit, ')', ' ', '9', ' ', digit, digit, digit, digit, '-', digit, digit, digit, digit];

  return (
    <div className="mb-3">
      <label className="form-label">{label}</label>
      {mask ? (
        <InputMask
          type={type}
          className="form-control"
          name={name}
          value={value}
          onChange={onChange}
          mask={mobileMask}
          placeholder={placeholder}
          required={required}
        />
      ) : (
        <input
          type={type}
          className="form-control"
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
        />
      )}
    </div>
  );
};
