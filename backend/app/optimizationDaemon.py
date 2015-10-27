__author__ = 'andreuke'
_building_ = "CSE"

from app.backend.commons.console import flash
from app.backend.controller.ruleOptimizer import RuleOptimizer

def start():
    flash("BuildingRules Optimizer is active...")

    ruleOptimizer = RuleOptimizer(_building_)
    ruleOptimizer.run()

