/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests/js'],
  testMatch: ['**/__tests__/**/*.(test|spec).(ts|tsx|js)'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'json'],
  moduleNameMapper: {
    // Map shared TypeScript path if imported like '@shared/...'
    '^@shared/(.*)$': '<rootDir>/shared/$1',
  },
  globals: {
    'ts-jest': {
      tsconfig: {
        target: 'ES2020',
        module: 'commonjs',
        esModuleInterop: true,
        strict: true,
        baseUrl: '.',
        paths: {
          '@shared/*': ['shared/*']
        }
      },
    },
  },
};
