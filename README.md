# skills

## Installation

### Ask your agent

Give a compatible coding agent this prompt to install the skills for the current project:

```text
Install the skills from https://github.com/molinfo-vienna/skills for this project.
```

### Use the Vercel Skills CLI

Install this skill repository and select skills interactively with

```bash
npx skills add https://github.com/molinfo-vienna/skills
```

If Vercel's `find-skills` helper is installed, you can also install a skill within an agent session:

```text
# Codex 
@find-skills cyp inhibition

# Agy
/find-skills cyp inhibition

# result
(Agent gives list of suitable skills)

# new prompt
Install the skill <skill-from-result-list>.
```

## Available skills

* nerdd-molecular-predictions: Access and use all prediction modules available on the live NERDD 
  web platform ([https://nerdd.univie.ac.at](https://nerdd.univie.ac.at)) or a local deployment. 
  For more information, see [the corresponding skill README](skills/nerdd-molecular-predictions/).

## Contribute

For adding a new skill you need to:

* fork and clone this repository
* add a new folder in `./skills` containing a file `SKILL.md`
* optionally add python scripts (with as few external dependencies as possible)
* push the changes to the fork and create a pull request
* note: basic correctness will be checked using `pre-commit run --all-files`
