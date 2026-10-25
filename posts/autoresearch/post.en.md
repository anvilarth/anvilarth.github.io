# Age of Autoresearch

_Andrey Filatov · 2026 · ~15 min read_

_Source: https://anvilarth.github.io/autoresearch.html · Author: Andrei Filatov (https://anvilarth.github.io/)_

## Chapter 1. A Lazy Evening

It was an ordinary weekday evening, and I was honestly too lazy to test hypotheses by hand.

Not lazy as in "tired and want to sleep" — lazy in a specific, engineering sense: I had a backlog of fifteen-ish ideas that needed to be run, checked, filtered for garbage, repeated. Work I'd done dozens of times and knew every step of by heart. And that evening I just didn't have it in me to sit down and click through the same thing manually one more time.

For the past month and a half I'd been living without weekends, trying to become a sort of 10x engineer — doing a lot more without raising my own cognitive load. Sounds nice. In practice it meant I was trying to shove agents into everything and hoping it would somehow speed itself up.

The first attempt was brazen and dumb at the same time: I just launched ten different tasks in parallel, agent upon agent. The logic was simple — if one agent handles one task fine, ten agents will handle ten tasks at once, and I get my evening back. In practice, almost always one of the ten broke. And the moment it broke, all of my attention got stuck on it. Net result: I spent more time cleaning up than if I'd just done them one by one myself. The aftertaste was mega unpleasant: I thought I'd split the work into parallel streams and instead got parallel chaos.

The second attempt was smarter. I figured — okay, if an agent without an explicit plan produces nonsense, I'll give it a plan. I wrote the agenda up front: what to do in which order, which corner cases to watch for, what counts as success. The agent behaved noticeably cleaner — fewer surprises, more cases covered. Things got better. But still kind of lousy — I was still sitting next to it cleaning up the loose ends, there were just fewer of them. It felt like I had improved the supervision process rather than gotten rid of the need to supervise.

And so on that lazy evening, instead of trying a third time to steer the agent better by hand, I did a lazy thing. I simply described my hypothesis-generation pipeline in text — how I usually come up with what to try next — and asked Gemini to evaluate the result of each attempt. Not to steer the process, not to decide the next step, but specifically to judge: here's a hypothesis, here's the result, is it good enough or not. I handed the whole thing to the agent and went to bed, because I was honestly too lazy to sit there and watch.

In the morning I opened the log and found that **40 hypotheses** had been tested overnight.

![Agent terminal: Pursuing goal (1d 1h 41m)](https://anvilarth.github.io/img/sankalp_17pm.webp)

_This is what it looks like from the outside: a line in the terminal and a counter ticking while you sleep. The screenshot isn't mine — it's from [sankalp's write-up](https://sankalp.bearblog.dev/autoresearch/), which is what the next chapter is about._

Not all forty turned out useful — some were outright garbage, some repeated what I'd already tried. But that didn't matter. All night I did nothing by hand — and came out with more tested variants than I'd have made in a week with a laptop. And it became clear: the point wasn't to steer the agent better. The point was who evaluates the result.

It worked once, at night, on one specific task. What remained was to understand what exactly had worked — and oddly enough, what helps you understand that isn't your own experience, but the fact that someone else had stumbled onto almost the same thing a bit before me.

## Chapter 2. It Already Had a Name

What happened that night wasn't an invention. It already had a name: autoresearch. And a couple of loud precedents before me.

First I came across [sankalp's post about QR decomposition](https://sankalp.bearblog.dev/autoresearch/). A classic task: decompose a matrix fast. He didn't touch the kernels by hand — he set Codex loose on the problem as an autonomous agent. It kept a beam of candidates, spawned sub-agents for profiling, math, and idea generation, and culled the dumb branches on its own as it went. The result — a **232x speedup** on batched QR and 12th place out of 183 participants, despite the author having no professional GPU experience.

![Beam search diagram: candidate branches, merge points, best branch](https://anvilarth.github.io/img/sankalp_10pm.webp)

_sankalp's beam of candidates: branches live in parallel, weak ones fade, strong ones merge. Nobody picks the winner by hand — the criterion picks it. Diagram from [sankalp's post](https://sankalp.bearblog.dev/autoresearch/)._

And as I read, it clicked that it wasn't about the agent or the prompt. Before, the expert invested in the solution itself: assembling features by hand, inventing heuristics from their head, writing kernels natively. Knowing how the problem worked was the job. Now that knowledge is almost unnecessary directly.

What you need is the ability to build a cycle that finds the solution itself: benchmark, oracle, stopping criterion. You don't write the kernel — you build the loop that searches through it. The same _bitter lesson_, just not about model architecture, but about what the human is busy with.

Two direct conclusions follow. First: you can physically do less work. That very hypothesis-testing routine I was too lazy to do in the evening gets delegated — the agent runs it at night, I sleep. Second: the work gets done better. Not "the same thing, faster," but qualitatively better — in the same time, the oracle searches the solution space wider than a single person and finds variants I simply would never have reached on my own.

And sankalp isn't the only one. Karpathy put together [autoresearch](https://github.com/karpathy/autoresearch): a 630-line script, an autonomous loop — the agent reads the training code, proposes a change, runs a five-minute run, measures the improvement, commits or rolls back, and goes again. Overnight — hundreds of experiments, not a single click. [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) from DeepMind — the same idea at a larger scale: Gemini plus an evolutionary framework plus automated evaluators. They improved solutions for 20% of 50 open mathematical problems, and sped up datacenters, chip design, and AI training at Google.

![autoresearch progress chart: 83 experiments, 15 kept improvements](https://anvilarth.github.io/img/karpathy_progress.png)

_One night in Karpathy's repo: 83 experiments, 15 of them kept improvements. The gray dots are what the loop culled on its own. Exactly the garbage proportion I saw in my log that morning. Chart from [karpathy/autoresearch](https://github.com/karpathy/autoresearch)._

In Karpathy's README there's a line that describes this shift more precisely than I'd formulated it myself:

> You're not touching any of the Python files like you normally would as a researcher. Instead, you are programming the `program.md` Markdown files that provide context to the AI agents and set up your autonomous research org.

The file the agent edits and the file the human edits are different files. All of the researcher's work has moved into the second one.

Different names, different implementations, different scale. But the same pattern: expertise moves from "find the solution" to "build the system that finds the solution."

And so far that's a frame, not an answer. To understand where the frame's edges are, what helped me wasn't other people's cases but two of my own. One went smoothly — there's almost nothing to tell about it. The second — the one where I had to argue with myself: I was sure I knew better.

## Chapter 3. I Knew Better

For two weeks I had been building dataset filters by hand.

A simple-looking task — decide which samples to throw out of training and which to keep. In practice, a mix of engineering and curation: you read papers, look at the data, formulate a hypothesis, test it, throw it away, repeat. I believed I understood this task. Armed with ego and knowledge of how to do it better, I spent two weeks pouring intuition and paper-reading into manual filters.

And then I did exactly what I did on that lazy evening — built a benchmark with Gemini as the oracle and set a zero-shot VLM loose on it. Just to see whether it would beat my manual work. No heuristics or hints, no involvement from me.

The first attempt was already better than two weeks of manual work. The second — even better.

It wasn't some cosmic gap. Not "the agent invented a filter I couldn't have thought of." The result was simply objectively better, and the time it took — a couple of runs versus two weeks of my life. And that's when it got genuinely painful — not because the method worked, but because I'd spent two weeks arguing with myself over a solution that the automation searched through in a couple of attempts.

Before AlexNet, features were assembled by hand. Engineers invented heuristics, picked out features, tuned pipelines — and that was expertise backed by years of work. Neural networks automated it: features became learned, and the work shifted to architecture and data. Now the researcher's expertise itself is being automated. You don't need to know the domain perfectly to make good decisions — it's enough to build an oracle that knows what counts as a good solution and let the agent run. That's the bitter lesson on my own skin. Two weeks beaten by a single night.

The second case went down much more calmly. Maybe the stakes were different — or maybe after the first one I stopped arguing with the oracle.

## Chapter 4. Not a Silver Bullet

The second case was about speeding up training. No inner drama — just a task where frontier models are expensive and can be overkill, but if you point them at optimizing inference or training time, they save money and time. I left the model working for two days and got a **30% speedup**. Pushing further got much harder, and there was no point spending more time on it. Smooth, mundane, no ego story.

But even on a smooth case — and especially afterward — pitfalls surfaced, the kind that mean this method shouldn't be treated as a silver bullet.

The first one — loss parity. I forgot to add a check to the oracle that the loss doesn't drift apart. The agent honestly reported "done, there's a speedup" — when in fact the loss was NaN everywhere. The model had formally become faster, but it had stopped learning. Once I added the loss parity check, the problem went away. A banal thing that I nonetheless missed, because I trusted the agent too much to decide what counts as success.

The second — an insufficiently detailed oracle. This surfaced later, on a text-removal-from-images task. I was testing different models but validating the result on the full image. Small artifacts — leftover letters, a half-erased character — I noticed with my eyes, but the oracle didn't. It considered the text removed, and the solution it called best in fact left garbage behind. As soon as I added a crop of the region where the text was supposed to be removed to the oracle — validating not the whole picture but the actual fact of removal — a completely different pipeline turned out to be the best. The previous winner had simply been exploiting the oracle's blindness.

![Chart of one session on KernelBench-Mega: speedup relative to reference versus tokens spent](https://anvilarth.github.io/img/kernelbench_session.jpg)

_What a properly built session looks like — a breakdown of one run on [KernelBench-Mega](https://kernelbench.com/mega). For the first 64% of the time there's no code at all: measuring the baseline, microbenchmarking barriers, deriving the roofline. The first working kernel appears at the 224k token mark. And near the end — the point I'm showing this for: "finer split-K regresses → measured, reverted". The hypothesis didn't work, the measurement caught it, rollback._

The benchmark's author describes that same run in one sentence:

> It spent 64% of the session in silence timing the baseline, microbenchmarking grid barriers, deriving a ~29x bytes/token roofline. The one regression it tried (finer split-K) it measured and reverted instead of rationalizing.

Measured and reverted instead of rationalizing — that's a working oracle. My NaN happened precisely because there was nothing to measure with, and rationalizing was all the agent had left.

The general lesson is simple and unpleasant: engineering autoresearch is a delicate task, where time should be spent specifically on designing the oracle and the loop. The time doesn't go into steering the agent or hunting for a magic prompt — it goes into honestly and thoroughly describing what counts as a good solution. Treating this as an automatic silver bullet means sooner or later getting a NaN where your loss used to be.

And even when the oracle is built right and the loop runs smoothly, one variable remains that design can't remove — the model inside the loop itself. I ran this whole finely-tuned process on different models, and it turned out that with the same oracle and the same task, the result depended not only on what I'd built, but on whom I'd entrusted it to.

## Chapter 5. Not Power, but Intuition

On the code-speedup task I had three models: Fable 5, Claude Opus 4.8, and GPT-5.5. Same task, same oracle.

Fable 5 — I just described the task, and everything worked. The agent produced hypotheses that made sense, tested them, culled the dumb ones. All I had left to do was nod at the reasonable steps. Claude Opus 4.8 proposed a solution that caused an OOM, and sort of gave up at that point — didn't correct itself, didn't try another path. GPT-5.5 eventually managed, but I had to explicitly point it where to look, otherwise it just treaded water.

The difference isn't in the ability to execute steps. All three can read code, write code, run, measure. The difference is in domain intuition — in how deeply the understanding of what's even worth trying in this task is baked into the model. Fable 5 had that understanding. The other two didn't.

I compensate for models' lack of intuition by throwing context into the prompt — blogs, guides, other people's cases. But that's a limitation, and an unpleasant one: to know what to help the model with, I have to already understand the topic well myself. In other words, the very expertise I thought I was automating, I have to keep in my head so I can pull it out in pieces and feed it to the agent.

And this isn't only my observation. The same pattern shows up in independent benchmarks. [KernelBench-Mega](https://kernelbench.com/mega) is a benchmark for whole-block megakernels, where you need to fuse an entire model block into one kernel rather than optimize individual operations. All previous models "won" on it only through a multi-kernel Triton pipeline — technically passes the test, but there's no honest fusion, it's a workaround. And only Fable 5, [according to the benchmark author's tweet](https://x.com/elliotarledge/status/2072814573753975266), wrote the first real megakernel. A direct parallel with my pitfall from chapter four: a poorly designed oracle allowed sleight of hand until someone did it honestly. [AutoKaggle](https://arxiv.org/abs/2410.20424) — the same pattern outside GPU: a multi-agent framework for Kaggle competitions, where the oracle is the competition itself and the tests, and across eight competitions it reached a 0.85 validation submission rate and 0.82 comprehensive score, at human level.

![Elliot Arledge's tweet about the first real megakernel](https://anvilarth.github.io/img/tweet_arledge.png)

_The benchmark author lists who "won" before and by how much: Opus 4.8 — 14.4x, GLM-5.2 — 11.1x, GPT-5.5 — 4.3x, Sonnet 5 — 4.0x. All through a multi-kernel Triton pipeline that doesn't pass the authenticity gate. [Full tweet](https://x.com/elliotarledge/status/2072814573753975266)._

So the best tool isn't the most powerful model — it's the model with the right intuition for the specific task. And the more precisely the oracle is built, the clearer you can see who has that intuition and who has to compensate for it with context.

Where this is heading is recursive loops — cycles where the agent improves not the model's weights but the system itself: the code, the pipeline, the artifact. Each improvement makes the next one easier. I hope tools you can simply use will appear soon. For now you have to pick which loop fits which task every time, and it works only in spots.

So what does that say about my own role, if intuition — the only thing that's still mine — is becoming a commodity you can just throw into a prompt?

## Chapter 6. What's Left

To the question "will AI replace us" I now have a boring answer: for part of the work, it already happened. Interns and juniors used to draw charts and test simple hypotheses — now the agent does all of that.

But that's about juniors. With me it's more complicated.

Three years ago I spent three days digging through PyTorch Lightning's source code to understand how checkpointing works there. Three days — and I knew it at a level where I could explain it to anyone and fix anything. Now an agent does the same in an hour. Frees you from the routine — yes. But takes something in return. That feeling of authorship that hand-digging through source code used to give — "I understood this, I did this" — it's gone. Factually, I did nothing, the agents did it all.

It's like moving from a senior role to a manager role. The story is exactly the same as in an ordinary career: you become a team lead — and you barely do anything with your own hands anymore. Before, you sat and solved things yourself; now you watch others solve them and make sure they solve them in the right direction. The output is more than you'd have made alone. But there's nothing hand-made by you in it anymore. The position is less dopaminergic: the old high from solving something with your own hands won't be there.

And I thought I could stop there. A manager is still needed, after all. Not because he's smarter than the people he manages, but because he knows where to point them — he has domain intuition. That was my conclusion in the previous chapter: the difference isn't power, it's intuition. Where the model lacks intuition, I compensate by throwing context into the prompt. Intuition was the last thing that was still mine. And then, over a couple of months, several stories piled up that don't fit this picture.

The Jacobian Conjecture — a classic conjecture in algebra. If a polynomial map has a nonzero constant Jacobian, then the map is invertible. Recently — a counterexample in dimension three. And it wasn't found by a group of mathematicians. It was found by Fable 5, while I was watching the World Cup final.

Terence Tao, a Fields Medal laureate, wrote a [post](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) to digest this. He explains retrospectively, geometrically, what the model found on its own. And here's what struck me: Tao sits down and counts just how improbable this is. A degree-seven polynomial. Its Jacobian has a priori up to **1329** nonzero coefficients — against **360** degrees of freedom of a general polynomial map of the same degree. 1329 equations that must vanish simultaneously, in a space of 360 variables. You don't find something like that by brute force — the chance of hitting the right point is zero. So Fable wasn't searching. It saw the structure.

![A paragraph from Terence Tao's post counting 1329 equations against 360 degrees of freedom](https://anvilarth.github.io/img/tao_1329.png)

_The very paragraph from [Tao](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/). The last sentence is a death sentence for brute force: "finding such a polynomial looks highly unlikely to be located by brute force"._

At the end of the post there's a disclaimer that five years ago would have looked wild in the text of a Fields medalist:

> I used an AI chatbot to discuss various aspects of this problem and to confirm several of the calculations made here.

Seeing where the solution lies in a space where naive search is useless. That's exactly what I considered mine.

In university they told me there are different levels of knowing the material. The first stage — you learn the terms: "Jacobian", "polynomial", "invertible map". You know they exist, but you don't understand them. The second — you know all the material: definitions, theorems, proofs. But you can't apply it — you bomb the exam problem because it differs slightly from the template. And there's a third stage, which is what actually knowing the material means — intuition. Not just knowing that a fact exists, but seeing when to apply it, and recognizing the same structure in a new situation.

Models have walked the same path. First stochastic parrots — guessing the next word. Then they learned the material, know the facts, but break on anything slightly new. And now — the third stage. They see structure, find solutions that weren't in the training data. A counterexample to a conjecture isn't a reproduction of something the model saw, it's new mathematics. And there's no cheating here: a counterexample either works or it doesn't — in pure mathematics there's no such thing as a badly designed oracle you can route around.

Fine, let's say the model has intuition. But the manager who points the way is still needed — that's what I was holding on to. The second case is exactly about this, and it's closer to me, because you can see what the human did there.

Mathematician Dmitry Rybin took the Dinits–Garg–Goemans conjecture — a problem about network flows, open since the nineties: can a fractional solution be made unsplittable without raising the cost and without overloading any edge by more than the size of the largest shipment. The counterexample was found by [GPT-5.6 Pro](https://chatgpt.com/share/6a60b2eb-0b64-83ee-9c76-7931ca1de063): a graph on seven nodes, three shipments, fractional cost 58, while any unsplittable routing costs at least 60.

![Counterexample to the Dinits–Garg–Goemans conjecture: a graph on seven nodes with flows, costs, and demands](https://anvilarth.github.io/img/rybin_graph.jpg)

_The entire counterexample in full: seven nodes, one source s, three sinks with demands 15, 10, and 15. Blue numbers are flow, red are edge costs. For thirty years nobody could either construct such a graph or prove it doesn't exist. [Image from Rybin's tweet](https://x.com/DmitryRybin1/status/2079904005652893709)._

What's interesting here isn't the model but the prompts. There were four of them, under sixty words in total: "construct a counterexample", "you should do a breakthrough", "it's enough of partial results, let's finish". Three sessions in a row, an hour and a half each, the model returned partial results, and the human simply asked it to continue. There is zero domain intuition in those words. There's direction, and an understanding of when the result is already good enough — that is, exactly what I'd kept for myself as the manager. Turns out, that's about a minute's worth of work.

The same skill transfers to my job too. My personal labor — what is it? A set of patterns I've built up over the years. "I've seen this bug — I know where to look." "This architecture breaks like this — route around it like this." "This hypothesis won't work because this metric lies." Those are all patterns. And patterns can be learned. And a network that found a solution in a space of 1329 equations — it will learn my patterns too. The only question is the price, and that price is cheaper every month than it was yesterday.

And here's the strange thing: the joy hasn't gone anywhere. I still open the log in the morning and stare at what happened overnight, even though I did nothing by hand. So the joy was never about "I solved it myself" — it was about the problem moving. And it moves a lot more now: I pull most of the model training alone, where a team used to be needed.

So I'm not quitting — I'm building the next loop. But to the question of where my value is now, I have no answer.

### Sources

- [sankalp — Auto-Research: QR Decomposition](https://sankalp.bearblog.dev/autoresearch/) — 232x speedup on batched QR (419,000 µs → 1805 µs) via Codex as an autonomous agent; 12th place among 183 participants, more than 1500 submissions in 14 days.

- [Andrej Karpathy — autoresearch](https://github.com/karpathy/autoresearch) — a 630-line script: training code → change → 5-minute run → improvement measure → commit/rollback → repeat.

- [DeepMind — AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) — Gemini + evolutionary framework + automated evaluators; improved solutions for 20% of 50 open mathematical problems.

- [Terence Tao — A digestion of the Jacobian conjecture counterexample](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) — counterexample in dimension 3; degree-7 polynomial, up to 1329 Jacobian coefficients against 360 degrees of freedom.

- [KernelBench-Mega](https://kernelbench.com/mega) — independent benchmark for whole-block megakernels (author: Elliot Arledge).

- [Elliot Arledge (tweet)](https://x.com/elliotarledge/status/2072814573753975266) — the first real megakernel on KernelBench-Mega, written by Fable 5.

- [AutoKaggle (arXiv:2410.20424)](https://arxiv.org/abs/2410.20424) — multi-agent framework for Kaggle competitions; 0.85 validation submission rate, 0.82 comprehensive score across 8 competitions.

- [Dmitry Rybin — counterexample to the Dinits–Garg–Goemans conjecture](https://chatgpt.com/share/6a60b2eb-0b64-83ee-9c76-7931ca1de063) — four prompts, under 60 words; three sessions with partial results, counterexample on the fourth: a graph on 7 nodes, three shipments, fractional cost 58 versus a minimum of 60 for any unsplittable routing.
