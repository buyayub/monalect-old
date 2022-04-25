### 2022.04.22

[9:03am]

Looking over my work yesterday, I'm a little unhappy with the design. It's acceptable, especially for a first one, but I think I need more media and need to make it more lively. I'll forego putting a personal video of it up there, just because my camera quality is horrible, and my editing sucks. I don't want to scare people away.  
I also can't spend too long working on this. Again, the point of working on the landing page, the blog, and so on is to establish the basic overall framework of the project. It'll be using static site generation for those two specifically, so creating a streamline of it from flask or node is not going to be helpful. 

I'll be throwing it up on Google Cloud as well, see how that works. 

A thing I have to think about is account management. I've accrued many google accounts over the days, and I'll need to consolidate them eventually, preferably before Monalect is seriously put out there so I won't have to rely on account changing features with stupid usernames. Perhaps a better way is to create rather a central document noting the account names and emails of the various business sites. So long as I have the map, I wouldn't really have to rely on a new series of accounts. It's also a bit counter-intuitive to fix my mess of accounts with more accounts.

[10:05am]

I'm unhappy with the design's visual scale. It's too large on my large monitor, but when I look at it on my laptop's smaller monitor, I find it just right.

I think I may cut some features as well. I find adding blog posts to be too much for now. The design works with just the minimum here.

[11:17am]

So far I'm happy with it. I'll put up the minimum touches, and move on. It's pretty minimal, but I expect to improve it later on when I have some of the main product to show off.

[8:18pm] 

I finished the design, and now I'm setting up the system. After playing around with staticjinja, I realized I could just do it myself in 5 lines of code, but regardless I encountered problems using the carbon design system. Namely, it's deep integration with Sass and the Node environment.

You see, my thought was I'd just load their processed css, load their processed javascript, be done with it. It is in fact not wise to do this. They want you to include components as you use them, for efficiency's sake. 

So in the end, I thought to just do it all in javascript. My discomfort with Node will just have to be set aside.

**Work Hours: 7 hours** (counts my pomodoro time)

### 2022.04.23

[12:00am]

It's midnight. I thought I'd wind down now and continue later. I've gotten everything. I made good progress today, specifically on utilizing the carbon design system. I can import their components, and manipulate them using SASS. I only really have to look out for javascript.

For tomorrow, I'll finish creating the statics for the landing page. I'll do it all by going through the html first, then connecting the components and seeing what breaks. It'll be interesting nonetheless.

I'm hoping this will make it easier on me in the future, but I still have the blog to go through, which will be a bit more complicated. I'm thinking EJS, the javascript templating engine I decided to go with, will make it easy. It's a question though. 

Utilizing React.js would make this so much easier, but I have a phobia of bloat. I keep remembering linkedin and reddit, and thinking how bad their frontend is using react. But there are also websites that do it well. Regardless, every React website had something iffy or somethign wrong with it. I don't want to suffer that. 

All this pain now is for relative ease later. My frontend will become a beautiful mess, but I can always clean it up as I move forward. My main concern is the seperation of concerns with the web app itself.

Anyways, I'm getting too tired to write. I'll update tomorrow.

[11:06am]

I'm starting a little late today, unfortunately. I have a dentist appointment at 3:45pm today that I'll be going to as well, which will take some time out of my day, but I'll go well into the night if I feel I haven't done enough today. 

Yesterday had been a little messy trying to figure out my frontend setup. I figured out how to use the Carbon Design System, but I'd still like to figure out SASS. I'd like to use webpack as well. I know make has a way you could watch files, but webpack has more features and options I'd like to use, and it's more fine-tuned towards watching. 

I'll be using webpack anyways when I use it for the javascript features.

So that'll be the start for today. I'll write it down here.

**Work Hours: 3 hours**

#### 2022.04.24

[12:14pm]

Didn't do a lot of work yesterday, but I knew to move onto Next.js, and now I'm figuring that out. 

One problem is that the carbon design system's react implementation uses an older version of react than what Next.js uses. There isn't much choice but to either roll back to an older version of React/Next, or to implement the components myself using their components package. I'm deciding to just roll back by installing @carbon/react first, then install next so that the package manager works out the dependencies, I hope. 

Another worry I have is that Next.js in exporting their static websites won't transfer javascript, or that the javascript it creates is embedded. It's a worry, but I won't truly know until I actually create the website. 

Next.js seems to be a full-stack implementation. I say that because it supports routing, user authentication, and whatnot. It also supports static html exports, which means they expect you to also use it to export for a static server if the website isn't complex. Thus I'll be constructing this in a full-stack environment for testing, then exporting the build when I'm done with it.

So for now, my main concern is just having the landing page setup using @carbon/react and Next.js in such a way that the architecture works. Today is that day, please god. 

This also makes it incredibly easy because I can just have next build my project to the static path for the web server everytime I update it with a blog post.

**Work Hours: 4 hours**

#### 2022.04.25

[3:19pm]

So today I did a bit of work. I "solved" everything with regards to actually setting up the html and css of the page. There's really only the javascript left to get confused by, but React and JSX is pretty straightforward. I've done it before, so it'll come to me pretty quickly.

My largest trouble today was just getting the animation to work. The first animation library which would transition text had a bug where if you centered your text, the angle of where the text would exit would change, so I opted out for a typing library, not wanting to debug it. 

There are a few spots of knowledge I'd like to remember and learn. I'm going through Next.js, SASS, and so forth by pure googling. I used to know React.js too, but the Next.js framework made everything alien again. Not entirely alien, but enough that I'm uncertain about a few things. 

Another thing is optimization. The amount of overhead for a landing page is ridiculous when built for production, nevermind the blog. I'll throw some numbers.

It makes 9 different requests for the javascript files, the largest of which is 408kb. My css file is 121kb. It also imports 9 different WOFF files. My wallpaper is less than half the size of the largest four files, which are javascript files and the css file. It's 50kb. I got away with it because I have a blurred background anyways, so I compressed the hell out of the jpeg.

I'll have to get down and dirty later on and optimize it, but it means knowing the ins and outs of Next.js and webpack. Going through the throttling mechanism in firefox's developer tools, wi-fi seems to work well enough that it loads in less than 300ms. On 3G-regular it took 8 seconds.

It's honestly mostly the fault of the browser loading in the background and fonts in last. If it loaded them first, there'd be barely any noticeable change in anything.

My code is also a little messy due to my inexperience with Sass and Next.js, but I know what next steps I can provide. If I decide to stick with it, I'll really want to know the ins-and-outs of everything so I can do well.

I think ultimately that's the better way to approach everything here. Use the established frameworks, then learn them inside and out, changing what I need so that I can optimize it. 

I know libraries tend to be replaced as time goes on, but highly-used libraries tend to keep going. The design structures will also be of help, moving onto them. But okay, I'm wasting time. Time to return to programming.
