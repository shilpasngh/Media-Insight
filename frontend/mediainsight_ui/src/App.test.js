import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

function sum(a, b) {
  return a + b;
}

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
})

// New tests
test('renders learn react link', () => {
  render(<App />);
  const title = screen.getByText(/Text to Image Generator/i);
  expect(title).toBeInTheDocument();
});


test('input field updates on change', () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/Enter text to generate image/i);
  
  fireEvent.change(input, { target: { value: 'Hello, World!' } });
  
  expect(input.value).toBe('Hello, World!');
});
