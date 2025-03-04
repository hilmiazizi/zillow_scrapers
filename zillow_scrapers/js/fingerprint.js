(function() {
    // GPU/Graphics card spoofing
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(param) {
        try {
        if (param === 37446) return "GeForce GTX 1080";
        if (param === 37445) return "NVIDIA Corporation";
        } catch (e) {
        console.error("WebGL Spoofing Error:", e);
        }
        return getParameter.apply(this, arguments);
    };

    // Webdriver
    delete Object.getPrototypeOf(navigator).webdriver;
    delete navigator.__webdriver_evaluate;
    delete navigator.__webdriver_script_evaluate;
    delete navigator.__webdriver_script_func;
    delete navigator.__webdriver_script_fn;
    delete navigator.__fxdriver_evaluate;
    delete navigator.__selenium_evaluate;
    delete navigator.__selenium_unwrapped;

    // Chrome object spoofing
    Object.defineProperty(window, 'chrome', {
      writable: false,
      configurable: false,
      value: {
        app: { isInstalled: false },
        runtime: {},
        loadTimes: () => { return {}; },
        csi: () => { return {}; }
      }
    });
    
    // Codecs
    const originalCanPlayType = HTMLMediaElement.prototype.canPlayType;
    HTMLMediaElement.prototype.canPlayType = function (type) {
        if (type.includes("mp4") || type.includes("h264")) {
            return "probably";
        }
        return originalCanPlayType.apply(this, arguments);
    };
    const originalIsTypeSupported = MediaSource.isTypeSupported;
    MediaSource.isTypeSupported = function (type) {
        if (type.includes("mp4") || type.includes("h264")) {
            return true;
        }
        return originalIsTypeSupported.apply(this, arguments);
    };

})();