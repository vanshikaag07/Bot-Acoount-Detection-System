"use client";

import { useState, type FormEvent } from "react";

const inputClass =
  "w-full rounded-lg border border-white/10 bg-navy px-4 py-3 text-ink placeholder:text-muted/60 focus:border-teal focus:outline-none focus:ring-2 focus:ring-teal/40";

export default function DemoForm() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    // TODO: send the form values to the trained model once it's deployed
    setSubmitted(true);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-white/10 bg-navy-light p-6 sm:p-8"
    >
      <label className="block">
        <span className="mb-2 block text-sm font-medium">Tweet text</span>
        <textarea
          name="tweet"
          required
          rows={4}
          placeholder="Paste a tweet from the account you want to check…"
          className={inputClass}
        />
      </label>

      <div className="mt-5 grid gap-5 sm:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm font-medium">Follower count</span>
          <input
            type="number"
            name="followers"
            min={0}
            required
            placeholder="e.g. 1200"
            className={inputClass}
          />
        </label>
        <label className="block">
          <span className="mb-2 block text-sm font-medium">Retweet count</span>
          <input
            type="number"
            name="retweets"
            min={0}
            required
            placeholder="e.g. 45"
            className={inputClass}
          />
        </label>
      </div>

      <button
        type="submit"
        className="mt-6 w-full rounded-lg bg-teal px-6 py-3 font-heading font-semibold text-navy transition hover:bg-teal-light"
      >
        Check this account
      </button>

      {submitted && (
        <p
          role="status"
          className="mt-5 rounded-lg border border-teal/40 bg-teal/10 px-4 py-3 text-sm"
        >
          Thanks! The detection model isn&apos;t connected yet — once it&apos;s
          live, you&apos;ll see a bot-likelihood score for this account here.
        </p>
      )}
    </form>
  );
}
