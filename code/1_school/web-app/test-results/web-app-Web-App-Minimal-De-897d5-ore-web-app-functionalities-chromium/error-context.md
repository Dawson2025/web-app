# Page snapshot

```yaml
- generic [ref=e1]:
  - navigation [ref=e2]:
    - link "My Web App" [ref=e3] [cursor=pointer]:
      - /url: /
    - generic [ref=e4]:
      - link "Dashboard" [ref=e5] [cursor=pointer]:
        - /url: /dashboard
      - link "Words" [ref=e6] [cursor=pointer]:
        - /url: /words
      - link "Log Out" [ref=e7] [cursor=pointer]:
        - /url: /logout
  - generic [ref=e8]:
    - heading "Words for \"My First Project\"" [level=2] [ref=e9]
    - heading "Add New Word" [level=3] [ref=e10]
    - generic [ref=e11]:
      - generic [ref=e12]: New Language Word
      - textbox "New Language Word" [active] [ref=e13]
      - generic [ref=e14]: English Translation
      - textbox "English Translation" [ref=e15]: Error Test
      - button "Add Word" [ref=e16] [cursor=pointer]
    - heading "Your Words" [level=3] [ref=e17]
    - paragraph [ref=e18]: No words added yet. Add some above!
```