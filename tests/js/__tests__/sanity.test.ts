describe('sanity', () => {
  it('true is truthy', () => {
    expect(true).toBeTruthy();
  });

  it('can import shared TS utils (once configured)', async () => {
    // This will work once ts-jest and path mapping are installed/configured in your environment
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const shared = await import('../../../shared/utils/typescript');
    expect(shared).toBeDefined();
  });
});
