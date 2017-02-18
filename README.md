# playing-with-python-on-ios

Sample project demonstrating Python on iOS, using native native UI (Apple UIKit).

## Notes

I'll try to show equivalent calls for Swift, Objective-C and Python.

Instantiate some class, that is create an object. `new` is same as `alloc+init` if no arguments are used.

```
# let x = UIViewController()
x = ObjCClass("UIViewController").new()
# UIViewController *x = [[UIViewController alloc] init];
x = ObjCClass("UIViewController").alloc().init()
```

Same with arguments

```
# let x = UINavigationController(rootViewController: root)
# INavigationController *x = [[UINavigationController alloc] initWithRootViewController: root];
x = ObjCClass("UINavigationController").alloc().initWithRootViewController_(root)
```

Colors

```
# UIColor.blue()
# [UIColor blueColor]
ObjCClass("UIColor").blueColor()
```
