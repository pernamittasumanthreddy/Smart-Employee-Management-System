from django.db import models
from django.utils.translation import gettext_lazy as _


class SkillProficiency(models.TextChoices):
    BEGINNER = 'BEGINNER', _('Beginner (Level 1)')
    INTERMEDIATE = 'INTERMEDIATE', _('Intermediate (Level 2)')
    ADVANCED = 'ADVANCED', _('Advanced (Level 3)')
    EXPERT = 'EXPERT', _('Expert (Level 4)')

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Skill Category')
        verbose_name_plural = _('Skill Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='employee_skills'
    )
    proficiency_level = models.CharField(
        max_length=20,
        choices=SkillProficiency.choices,
        default=SkillProficiency.INTERMEDIATE
    )
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_skills'
    )

    class Meta:
        verbose_name = _('Employee Skill')
        verbose_name_plural = _('Employee Skills')
        unique_together = ('employee', 'skill')
        ordering = ['employee', '-proficiency_level']

    def __str__(self):
        return f"{self.employee.full_name} - {self.skill.name} ({self.get_proficiency_level_display()})"


class ProjectSkillRequirement(models.Model):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='required_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='project_requirements'
    )
    min_proficiency = models.CharField(
        max_length=20,
        choices=SkillProficiency.choices,
        default=SkillProficiency.INTERMEDIATE
    )

    class Meta:
        verbose_name = _('Project Skill Requirement')
        verbose_name_plural = _('Project Skill Requirements')
        unique_together = ('project', 'skill')

    def __str__(self):
        return f"{self.project.name} requires {self.skill.name} ({self.min_proficiency})"
