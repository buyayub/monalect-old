/* eslint-disable */
import {
	Header, 
	HeaderName, 
	HeaderNavigation, 
	HeaderMenuItem,
	Theme,
	TextInput,
	Button,
	Layer,
	TextArea
} from '@carbon/react/';

import {
	LogoTwitter,
	LogoGithub,
	LogoYoutube,
	LogoFacebook,
	Email,
	DocumentAdd,
	CloudUpload,
	Template,
	Notebook,
	Help,
	Link
} from '@carbon/icons-react/';

import TypeAnimation from 'react-type-animation';


function Landing() {

	const TEXTS = [
		"math", 1000,
		"programming", 1000,
		"philosophy", 1000,
		"physics", 1000,
		"chemistry", 1000,
		"psychology", 1000
	];

	return (
		<Theme theme="g100" >
			<Header aria-label="" aria-labelledby="">
				<HeaderName href="#" prefix="MONALECT" children=""></HeaderName>
				<HeaderNavigation aria-label="Landing">
					<HeaderMenuItem href = "#">
						Blog
					</HeaderMenuItem>
					<HeaderMenuItem href = "#">
						Plans
					</HeaderMenuItem>
					<HeaderMenuItem href = "#">
						About
					</HeaderMenuItem>
				</HeaderNavigation>
			</Header>
			<main>
				<section id="eye-catch">
					<h3>Tired of other people's courses?</h3>
					<h3><b>Create your own.</b></h3>
					<div>
						<h4>
							Self study &nbsp;
							<TypeAnimation
								cursor = {false}
								sequence={TEXTS}
								repeat={Infinity}
								className="subjects-animation"
								/> 
							&nbsp; for free with our app. 
						</h4>
						<h4> Upload learning materials, organize your lessons, and then we take care of the rest.</h4>
					</div>
					<h4>All <em>you</em> have to do is study.</h4>
					<div className="email-input">
						<Theme theme="white">
							<TextInput
								id="email-input"
								type="text"
								labelText="Email"
								placeholder="Email..." 
							/>
						</Theme>
						<Button size="md" className="email-input-button">Get Notified</Button>
					</div>
					<h3> Coming Soon </h3>
					<div className="social">
						<LogoTwitter size={64} />
						<LogoGithub size={64} />
						<LogoYoutube size={64} />
						<Email size={64} />
					</div>
				</section>
				<article className="landing-article">
					<h4> You can create, manage, and share your own courses</h4>
					<p> There is an endless amount of learning resources and learning materials online-- more than enough for an autodidact to study-- but there has never been an all encompassing tool to study it. So without sacrificing the freedom you have when studying personal learning materials, we provide you with multiple tools to study and measure your progress under a single cohesive learning environment. Study without feeling like you're scattered, or lost. </p>
				</article>
				<section id="features">
					<h3> Initial Features </h3>
					<div class= "feature-list">
						<div class="feature-item">
							<DocumentAdd size={64} />
							<p> Create courses quickly and effortlessly. </p>
						</div>
						<div class="feature-item">
							<CloudUpload size={64} />
							<p> Upload your own books and articles to use within the course.</p>
						</div>
						<div class="feature-item">
							<Template size={64} />
							<p> Not enough time to create? You can use one of our templates. Questions are included, and the textbooks are free! </p>
						</div>
						<div class="feature-item">
							<Notebook size={64} />
							<p> Practice and review your previous courses to keep your knowledge fresh </p>
						</div>
						<div class="feature-item">
							<Help size={64} />
							<p> Create questions and then test yourself later to see whether you're ready to move on. </p>
						</div>
					</div>
				</section>
				<section id="final">
					<div id="vision-share">
						<div id="vision">
							<h3>Our Vision:</h3>
							<p> We hope to create a free social network for learning run by our users. We believe people have a right to a post-secondary education without being encumbered by the expenses, and we'll try to give access to that right here with Monalect. Poor or rich, you deserve the right to learn. </p>
						</div>
						<div class="share">
							<h3> Share us: </h3>
							<div>
								<LogoTwitter size={48} />
								<LogoFacebook size={48} />
								<Email size={48} />
								<Link size={48} />
							</div>
						</div>
					</div>
					<div class="suggestion-form">
						<Theme theme="white">
							<TextArea 
								labelText="We welcome suggestions!"
								placeholder="Write here..."
								maxCount={500}
								enableCounter={true}
								cols={50}
								rows={6}
								id="suggestion-box"
								light={true}
							/>	
						</Theme>
						<Button size="md" className="suggestion-form-button">Submit</Button>
					</div>
				</section>
				<footer>
					<p> Created by <a href="https://www.github.com/buyayub">Ayub Elwhishi</a> using the <a href="https://github.com/carbon-design-system/carbon"> Carbon Design System</a></p>
				</footer>
			</main> 
		</Theme> 
	)
}

export default Landing
