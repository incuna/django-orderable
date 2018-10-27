Feature: Ordering on the list page

  Scenario: Move an item to the end of the list
    Given the following items:
      | pk |
      |  1 |
      |  2 |
      |  3 |
    And we are on the item list page
    When item 1 is moved to position 3
    Then the items should be ordered thus:
      | pk |
      |  2 |
      |  3 |
      |  1 |

  Scenario: Move an item to the top of the list
    Given the following items:
      | pk |
      |  1 |
      |  2 |
      |  3 |
    And we are on the item list page
    When item 3 is moved to position 1
    Then the items should be ordered thus:
      | pk |
      |  3 |
      |  1 |
      |  2 |
