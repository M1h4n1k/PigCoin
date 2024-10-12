interface HTMLElementInfiniteScroll extends HTMLElement {
  __scrollHandler__?: () => void;
}

const windowScroller = (el: HTMLElementInfiniteScroll, func: () => void) => {
  if (document.body.scrollTop + window.innerHeight >= el.clientHeight - 100) {
    func();
  }
};

const vInfiniteScroll = {
  mounted(el: HTMLElementInfiniteScroll, binding: any) {
    const scrollHandler = () => windowScroller(el, binding.value);
    el.__scrollHandler__ = scrollHandler;
    document.body.addEventListener("scroll", scrollHandler);
  },
  unmounted(el: HTMLElementInfiniteScroll) {
    document.body.removeEventListener("scroll", el.__scrollHandler__!);
  },
};

export { vInfiniteScroll };
