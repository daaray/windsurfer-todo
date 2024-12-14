import { config } from '@vue/test-utils';
import { Quasar } from 'quasar';
import { vi } from 'vitest';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock Quasar plugins
const plugins = {
  Notify: {
    create: vi.fn(),
  },
};

config.global.plugins = [
  [
    Quasar,
    {
      plugins,
      config: {
        dark: 'auto',
      },
    },
  ],
];

// Mock Notify globally
vi.mock('quasar', async () => {
  const actual = await vi.importActual('quasar');
  return {
    ...actual,
    Notify: {
      create: vi.fn(),
    },
  };
});
