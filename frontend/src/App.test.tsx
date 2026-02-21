import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders UEP platform', () => {
  render(<App />);
  const heading = screen.getByText(/UEP v5\.0/i);
  expect(heading).toBeInTheDocument();
});
