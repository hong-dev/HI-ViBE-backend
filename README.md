# Introduction
- [VIBE web site](https://vibe.naver.com/) clone project
- Developed by a team of 6 developers (3 Front-End, 1 React Native, 2 Back-End)
- [Front-End GitHub Repository](https://github.com/wecode-bootcamp-korea/HI-VIBE-frontend) / [React Native GitHub Repository](https://github.com/wecode-bootcamp-korea/HI-ViBE-app)

# Demo
[![HI-VIBE Demo Video](https://images.velog.io/images/aerirang647/post/88e2b424-dc6d-40f9-b6bd-6ec52e9247b1/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202020-03-22%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.52.30.png)](https://vimeo.com/399385820)

# Technologies
- Frontend : React.js, TypeScript, Styled Component, Redux, React-Native
- Backend : Python, Django, MySQL, CORS headers
- Deployment : AWS

# Features/APIs
### Data / Deploy
* Web Crawling : used xmltodict for XML APIs
* Deployment : AWS EC2(Server), RDS(Database)

### User
* Sign in : Naver social log-in API, used JWT for generating token

### Music
* Station Theme: change themes, save selected theme in database
* Magazine, Recommendation, LatestAlbum, News, Video, Genre list
* Search : return music, album, video, lyrics list which contain keyword in their name or lyrics
* Music list in selected Recommendation, Station, Album, Artist
* Music, Artist Details
* Streaming : used open(), read(), StreamingHttpResponse
* Ranking : Album, Domestic album, Foreign album lists ordered by likes count

# API Documentation
[Endpoint API Documentation using Postman](https://documenter.getpostman.com/view/10633619/SzS2xob4?version=latest)

# Database Modeling
![Modeling using aquery](https://user-images.githubusercontent.com/53142539/76675121-89b7af00-65f9-11ea-9a5b-2c531b5d5b89.png)
