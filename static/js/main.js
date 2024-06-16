if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.register('/service-worker.js')
    .then(function(swReg) {
        console.log('Service Worker is registered', swReg);

        swReg.pushManager.getSubscription()
        .then(function(subscription) {
            if (subscription === null) {
                swReg.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: 'YOUR_PUBLIC_VAPID_KEY'
                }).then(function(subscription) {
                    console.log('User is subscribed:', subscription);

                    fetch('/subscribe', {
                        method: 'POST',
                        body: JSON.stringify(subscription),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                });
            }
        });
    })
    .catch(function(error) {
        console.error('Service Worker Error', error);
    });
}
