//fridatest.js
Java.perform(function () {
    var TargetClass = Java.use('com.ldjSxw.heBbQd.a.b');
    TargetClass.k.implementation = function () {
        console.log('inject');
        return false;
    };
});
