#include <cassert>
#include <iostream>
#include <cmath>
#include <iomanip>

#include "../src/red_black_tree.cpp"

void printTestHeader(const std::string &testName) {
    std::cout << "\n========================================\n";
    std::cout << "=== " << testName << " ===" << std::endl;
    std::cout << "========================================\n";
}

void printSuccess() {
    std::cout << "[PASS]" << std::endl;
}

void testing() {
    RBTree rb_tree;

    printTestHeader("1. Basic Insertion and Rating Check");
    rb_tree.insert("Inception", 8.8);
    rb_tree.insert("The Dark Knight", 9.0);
    rb_tree.insert("Interstellar", 8.6);

    assert(rb_tree.search("Inception") != nullptr);
    assert(rb_tree.search("The Dark Knight") != nullptr);
    assert(rb_tree.search("Interstellar") != nullptr);
    assert(rb_tree.search("Nonexistent Movie") == nullptr);

    std::cout << "Checking ratings:" << std::endl;
    std::cout << "  Inception: " << std::fixed << std::setprecision(1)
            << rb_tree.search("Inception")->avg_rating << std::endl;
    std::cout << "  The Dark Knight: "
            << rb_tree.search("The Dark Knight")->avg_rating << std::endl;
    std::cout << "  Interstellar: "
            << rb_tree.search("Interstellar")->avg_rating << std::endl;
    printSuccess();

    printTestHeader("2. Updating Average Rating");
    rb_tree.insert("Inception", 9.2);
    const Node *inception = rb_tree.search("Inception");
    std::cout << "New rating for Inception: "
            << inception->avg_rating << std::endl;
    assert(std::abs(inception->avg_rating - 9.0) < 1e-6);
    printSuccess();

    printTestHeader("3. Recommendation System Check");
    const Node *recommendation = rb_tree.recommend(8.5);
    assert(recommendation != nullptr);
    std::cout << "Recommended movie: " << recommendation->film_name
            << " (rating: " << recommendation->avg_rating << ")" << std::endl;
    printSuccess();

    printTestHeader("4. Red-Black Tree Properties Validation");
    auto checkRBProperties = [](Node *node, int blackCount, int currentCount, auto &&self) {
        if (!node) {
            if (blackCount == -1) blackCount = currentCount;
            assert(currentCount == blackCount);
            return;
        }
        if (node->color == RED) {
            assert(!node->left || node->left->color == BLACK);
            assert(!node->right || node->right->color == BLACK);
        }
        int newCount = currentCount + (node->color == BLACK ? 1 : 0);
        self(node->left, blackCount, newCount, self);
        self(node->right, blackCount, newCount, self);
    };
    checkRBProperties(rb_tree.root, -1, 0, checkRBProperties);
    std::cout << "All properties are valid" << std::endl;
    printSuccess();

    printTestHeader("5. Recommendation for an Empty Tree");
    RBTree emptyTree;
    assert(emptyTree.recommend(5.0) == nullptr);
    std::cout << "Empty tree recommendations are correct" << std::endl;
    printSuccess();

    printTestHeader("6. Handling Negative Ratings");
    rb_tree.insert("Negative Movie", -5.0);
    rb_tree.insert("Negative Movie", -3.0);
    const Node *negative = rb_tree.search("Negative Movie");
    std::cout << "Average rating for 'Negative Movie': "
            << negative->avg_rating << std::endl;
    assert(negative->count_ratings == 2);
    assert(std::abs(negative->avg_rating - (-4.0)) < 1e-6);
    printSuccess();

    printTestHeader("7. Maximum Rating Value Test");
    rb_tree.insert("Max Rating Film", std::numeric_limits<double>::max());
    const Node *maxRating = rb_tree.search("Max Rating Film");
    std::cout << "Maximum rating: "
            << maxRating->avg_rating << std::endl;
    assert(maxRating->avg_rating == std::numeric_limits<double>::max());
    printSuccess();

    printTestHeader("8. Recommendations with Identical Ratings");
    rb_tree.insert("Twin A", 8.4);
    rb_tree.insert("Twin B", 8.4);
    const Node *twinRec = rb_tree.recommend(8.4);
    assert(twinRec != nullptr);
    assert(twinRec->avg_rating == 8.4);
    std::cout << "Selected recommendation: " << twinRec->film_name
            << "\n";
    printSuccess();

    std::cout << "\n========================================\n";
    std::cout << "  ALL 8 TESTS PASSED SUCCESSFULLY!" << std::endl;
    std::cout << "========================================\n\n";
}

int main() {
    testing();
    return 0;
}
