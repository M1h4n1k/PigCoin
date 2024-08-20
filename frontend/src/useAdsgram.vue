<script lang="ts">
import { ref } from "vue";

export function useAdsgram({ blockId, onReward, onError }) {
  const AdControllerRef = ref(null);

  AdControllerRef.value = window.Adsgram.init({
    blockId: blockId,
    debug: true,
  });

  const showAd = () => {
    if (AdControllerRef.value) {
      AdControllerRef.value
        .show()
        .then(() => {
          onReward();
        })
        .catch((result) => {
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
</script>
