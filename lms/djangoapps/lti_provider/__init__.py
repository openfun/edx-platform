"""
The LTI Provider app gives a way to launch edX content via a campus LMS
platform. LTI is a standard protocol for connecting educational tools, defined
by IMS:
    http://www.imsglobal.org/toolsinteroperability2.cfm
"""

# Import the tasks module to ensure that signal handlers are registered.
import lms.djangoapps.lti_provider.tasks
