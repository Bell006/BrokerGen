export const Dropdown = ({ label, options, value, onChange, disabled, placeholder }) => {
  return (
    <div className="mb-3">
      <label className="form-label text-light">{label}</label>
      <select
        className="form-select"
        value={value}
        onChange={onChange}
        disabled={disabled}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};
