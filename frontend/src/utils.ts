const getRandomNumber = (
  min: number,
  max: number,
  previous: number,
  delta: number,
): number => {
  let random = Math.floor(Math.random() * (max - min + 1)) + min;
  while (Math.abs(random - previous) < delta) {
    random = Math.floor(Math.random() * (max - min + 1)) + min;
  }
  return random;
};

export { getRandomNumber };
