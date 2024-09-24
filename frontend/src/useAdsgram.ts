import { ref } from "vue";
import { AdsgramController } from "@/types.ts";

export function useAdsgram({
  blockId,
  onReward,
  onError,
}: {
  blockId: string;
  onReward: () => void;
  onError: (result: any) => void;
}) {
  const AdControllerRef = ref<AdsgramController>(
    window.Adsgram.init({
      blockId: blockId,
      // debug: true,
    }),
  );

  const showAd = () => {
    if (AdControllerRef.value) {
      AdControllerRef.value
        .show()
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
