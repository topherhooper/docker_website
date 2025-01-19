import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import ChatInput from '../ChatInput';

describe('ChatInput', () => {
  const mockSendMessage = jest.fn();

  beforeEach(() => {
    // Clear mock calls between tests
    mockSendMessage.mockClear();
  });

  test('renders input and button', () => {
    render(<ChatInput onSendMessage={mockSendMessage} />);
    
    const input = screen.getByPlaceholderText('Type your message...');
    const button = screen.getByRole('button');
    
    expect(input).toBeInTheDocument();
    expect(button).toBeInTheDocument();
    expect(input).toBeEnabled();
    expect(button).toBeEnabled();
  });

  test('calls onSendMessage when form is submitted', () => {
    render(<ChatInput onSendMessage={mockSendMessage} />);
    
    const input = screen.getByPlaceholderText('Type your message...');
    const testMessage = 'test message';
    
    fireEvent.change(input, { target: { value: testMessage } });
    fireEvent.submit(input.closest('form'));
    
    expect(mockSendMessage).toHaveBeenCalledTimes(1);
    expect(mockSendMessage).toHaveBeenCalledWith(testMessage);
  });

  test('does not call onSendMessage when empty message is submitted', () => {
    render(<ChatInput onSendMessage={mockSendMessage} />);
    
    const input = screen.getByPlaceholderText('Type your message...');
    fireEvent.submit(input.closest('form'));
    
    expect(mockSendMessage).not.toHaveBeenCalled();
  });

  test('clears input after successful submission', () => {
    render(<ChatInput onSendMessage={mockSendMessage} />);
    
    const input = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(input, { target: { value: 'test message' } });
    fireEvent.submit(input.closest('form'));
    
    expect(input.value).toBe('');
  });

  test('disables input and button when disabled prop is true', () => {
    render(<ChatInput onSendMessage={mockSendMessage} disabled={true} />);
    
    expect(screen.getByPlaceholderText('Type your message...')).toBeDisabled();
    expect(screen.getByRole('button')).toBeDisabled();
  });
});