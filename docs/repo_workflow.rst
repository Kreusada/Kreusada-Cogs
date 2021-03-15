.. _workflow:

================
Project Workflow
================

I like to add my issues and PRs to my project named 'Workflow',
it helps to keep track of everything I need to get through.

There are four sections:

* To do
* In progress
* Done
* Rejected/Infeasible

If your issue/PR is in the ``To do`` section, that means that I haven't
started looking at it. The issue/PR will have one of the following status labels:

* Status: Lamented
* Status: Processing
* Status: Triage Requested
* Status: Requested Changes (PR Only)

If your issue/PR is in the ``In progress`` section, that means that I have started to 
outline, test or develop the requested changes. The issue/PR will have one of the following status labels:

* Status: Admin
* Status: Progress

If your issue/PR is in the ``Done`` section, that means the requested changes have been implemented or merged!
The issue/PR will have one of the following status labels:

* Status: Passed

If your issue/PR is in the ``Rejected/Infeasible`` section, that means I am not making changes.
The issue/PR will have one of the following status labels:

* Status: Rejected
* Status: Infeasible
* Status: Withdrawn

There is one more status label which hasn't been mentioned yet, which is ``Status: Expansive``.
In order to have this label added, the initial changes must have the ``Status: Passed`` label.
When the PR/issue has passed, and there are additional requested changes, the issue/PR will
move back down to ``To do``, or ``In progress``, where it will continue its development with
the expansive label.

Please avoid elaborating profusely on original issues/PRs with outlined changes. I would much prefer
it that you opened a new issue/PR with the requested changes, so that we won't even need to use the 
expansive label.
