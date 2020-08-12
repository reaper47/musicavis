from django.test import TestCase
from django.urls import reverse


class LegalViewsTests(TestCase):
    def test_privacy(self):
        """
        WHEN requesting the privacy policy
        THEN display the privacy policy
        """
        response = self.client.get(reverse("app:legal.privacy"))

        data = [
            "Privacy Policy",
            "we collect",
            "What do you do",
            "information secure",
            "about cookies",
            "any question",
        ]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all([x.encode() in response.content for x in data]))

    def test_terms(self):
        """
        WHEN requesting the terms of use
        THEN display the terms of use
        """
        response = self.client.get(reverse("app:legal.terms"))

        data = [
            "Terms of Use",
            "General Information",
            "Copyright and Trademark Notice",
            "External Links",
            "Membership Eligibility",
            "Fees and Services",
            "No Warranty",
            "Liability Limit",
            "Jurisdiction",
            "Revisions",
            "Privacy Policy",
            "Personal Information",
        ]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all([x.encode() in response.content for x in data]))
