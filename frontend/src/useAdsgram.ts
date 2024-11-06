export function useAdsgram({
  blockId,
  onReward,
  onError,
}: {
  blockId: string;
  onReward: () => void;
  onError: (result: any) => void;
}) {
  const AdControllerRef = window.Adsgram.init({
    blockId: blockId,
    // debug: true,
  });

  const showAd = () => {
    if (AdControllerRef) {
      AdControllerRef.show()
        .then(() => {
          onReward();
        })
        .catch((result: any) => {
          onError?.(result);
        });
    } else {
      onError?.({
        error: true,
        done: false,
        state: "load",
        description: "Adsgram script not loaded",
      });
    }
  };

  return { showAd };
}
