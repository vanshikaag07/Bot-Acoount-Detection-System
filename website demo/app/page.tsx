import DemoForm from "@/components/DemoForm";

const navLinks = [
  { href: "#problem", label: "Problem" },
  { href: "#how-it-works", label: "How it works" },
  { href: "#demo", label: "Try it" },
  { href: "#team", label: "Team" },
];

const problems = [
  {
    title: "Disinformation",
    body: "Coordinated bot networks amplify false narratives, making fringe claims look like widespread opinion.",
  },
  {
    title: "Financial fraud",
    body: "Fake accounts push scams, pump-and-dump schemes, and phishing links to unsuspecting users.",
  },
  {
    title: "Data contamination",
    body: "Bot activity skews the social media data that researchers, brands, and models rely on.",
  },
];

const signals = [
  {
    title: "Behavioral signals",
    body: "How an account acts says a lot about who runs it.",
    items: ["Follower count", "Retweet ratio", "Account age"],
  },
  {
    title: "Writing style",
    body: "Bots tend to write in recognizable ways.",
    items: [
      "Repetitive phrasing and templates",
      "Hashtag and link density",
      "Unnatural text patterns",
    ],
  },
];

const stats = [
  { value: "50K", label: "Labeled records" },
  { value: "10", label: "Features" },
  { value: "Kaggle", label: "Data source" },
];

const team = [
  { name: "Kavin Rajesh"},
  { name: "Vanshika Agarwal"},
  { name: "Maggie Tobacco"},
  { name: "Liam Flemming"},
];

function initials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("");
}

function SectionHeading({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <p className="text-sm font-semibold uppercase tracking-widest text-teal">
        {eyebrow}
      </p>
      <h2 className="mt-3 font-heading text-3xl font-semibold sm:text-4xl">
        {title}
      </h2>
      {children && <p className="mt-4 text-muted">{children}</p>}
    </div>
  );
}

export default function Home() {
  return (
    <>
      {/* 1. Sticky nav */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-navy/80 backdrop-blur">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <a href="#" className="font-heading text-xl font-bold tracking-tight">
            AI4<span className="text-teal">SMA</span>
          </a>
          <ul className="flex gap-4 text-sm text-muted sm:gap-8">
            {navLinks.map((link) => (
              <li key={link.href}>
                <a href={link.href} className="transition hover:text-ink">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main>
        {/* 2. Hero */}
        <section className="relative overflow-hidden">
          <div
            aria-hidden
            className="pointer-events-none absolute left-1/2 top-0 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-teal/15 blur-3xl"
          />
          <div className="relative mx-auto max-w-4xl px-4 py-28 text-center sm:px-6 sm:py-36">
            <p className="text-sm font-semibold uppercase tracking-widest text-teal">
              Purdue VIP · AI for Social Media Analysis
            </p>
            <h1 className="mt-5 font-heading text-4xl font-bold leading-tight sm:text-6xl">
              Is that account real — or a bot?
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted">
              AI4SMA uses machine learning to flag bot and fake accounts on
              Twitter/X by combining how an account behaves with how it writes.
            </p>
            <a
              href="#demo"
              className="mt-10 inline-block rounded-lg bg-teal px-8 py-3 font-heading font-semibold text-navy transition hover:bg-teal-light"
            >
              Try the demo
            </a>
          </div>
        </section>

        {/* 3. Problem */}
        <section id="problem" className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
          <SectionHeading eyebrow="The problem" title="Why fake accounts matter">
            Bots and fake profiles make up a meaningful share of activity on
            social platforms. Left unchecked, they distort what people see and
            what researchers measure.
          </SectionHeading>
          <div className="mt-14 grid gap-6 md:grid-cols-3">
            {problems.map((p) => (
              <div
                key={p.title}
                className="rounded-2xl border border-white/10 bg-navy-light p-6"
              >
                <div className="mb-4 h-1 w-10 rounded-full bg-teal" />
                <h3 className="font-heading text-lg font-semibold">{p.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  {p.body}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* 4. How it works */}
        <section
          id="how-it-works"
          className="mx-auto max-w-6xl px-4 py-24 sm:px-6"
        >
          <SectionHeading eyebrow="How it works" title="Two lenses on every account">
            Our model looks at an account from two angles and combines them
            into a single prediction.
          </SectionHeading>
          <div className="mt-14 grid gap-6 md:grid-cols-2">
            {signals.map((s) => (
              <div
                key={s.title}
                className="rounded-2xl border border-white/10 bg-navy-light p-8"
              >
                <h3 className="font-heading text-2xl font-semibold">{s.title}</h3>
                <p className="mt-2 text-muted">{s.body}</p>
                <ul className="mt-6 space-y-3">
                  {s.items.map((item) => (
                    <li key={item} className="flex items-center gap-3">
                      <span className="h-2 w-2 shrink-0 rounded-full bg-teal" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* 5. Dataset stats */}
        <section className="border-y border-white/10 bg-navy-light">
          <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 text-center sm:grid-cols-3 sm:px-6">
            {stats.map((s) => (
              <div key={s.label}>
                <p className="font-heading text-4xl font-bold text-teal sm:text-5xl">
                  {s.value}
                </p>
                <p className="mt-2 text-sm uppercase tracking-widest text-muted">
                  {s.label}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* 6. Demo */}
        <section id="demo" className="mx-auto max-w-3xl px-4 py-24 sm:px-6">
          <SectionHeading eyebrow="Try it" title="Check an account">
            Enter a tweet and a couple of account stats. The live model is
            still in training, so results are coming soon.
          </SectionHeading>
          <div className="mt-12">
            <DemoForm />
          </div>
        </section>

        {/* 7. Team */}
        <section id="team" className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
          <SectionHeading eyebrow="Team" title="Who's building AI4SMA" />
          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {team.map((member) => (
              <div
                key={member.name}
                className="rounded-2xl border border-white/10 bg-navy-light p-6 text-center"
              >
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-teal/20 font-heading text-lg font-semibold text-teal">
                  {initials(member.name)}
                </div>
                <h3 className="mt-4 font-heading font-semibold">{member.name}</h3>
                
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* 8. Footer */}
      <footer className="border-t border-white/10">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 py-8 text-sm text-muted sm:flex-row sm:px-6">
          <p>
            <span className="font-heading font-semibold text-ink">AI4SMA</span>{" "}
            · Purdue VIP · {new Date().getFullYear()}
          </p>
          {/* TODO: replace with the real repository URL */}
          <a href="#" className="transition hover:text-teal">
            GitHub
          </a>
        </div>
      </footer>
    </>
  );
}
