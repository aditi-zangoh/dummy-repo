import { CapitalizePipe } from './capitalize.pipe';

describe('CapitalizePipe', () => {
  let pipe: CapitalizePipe;

  beforeEach(() => {
    pipe = new CapitalizePipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });

  it('should capitalize first letter of a word', () => {
    expect(pipe.transform('hello')).toBe('Hello');
  });

  it('should capitalize first letter and lowercase the rest', () => {
    expect(pipe.transform('HELLO')).toBe('Hello');
    expect(pipe.transform('hELLO')).toBe('Hello');
  });

  it('should handle empty string', () => {
    expect(pipe.transform('')).toBe('');
  });

  it('should handle null and undefined', () => {
    expect(pipe.transform(null)).toBe('');
    expect(pipe.transform(undefined)).toBe('');
  });

  it('should handle single character', () => {
    expect(pipe.transform('a')).toBe('A');
    expect(pipe.transform('Z')).toBe('Z');
  });

  it('should handle strings with spaces', () => {
    expect(pipe.transform('hello world')).toBe('Hello world');
  });

  it('should handle strings starting with non-alphabetic characters', () => {
    expect(pipe.transform('123abc')).toBe('123abc');
    expect(pipe.transform('!hello')).toBe('!hello');
  });

  it('should handle multiple words but only capitalize first', () => {
    expect(pipe.transform('hello WORLD test')).toBe('Hello world test');
  });
});
