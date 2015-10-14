<?php

require_once '../bootstrap.php';

class RecipeParser_Canonical_Test extends PHPUnit_Framework_TestCase {

    /**
     * @group network
     */
    public function test_m_dot_allrecipes() {
        $url       = "http://m.allrecipes.com/recipe/70343/slow-cooker-chicken-taco-soup/";
        $canonical = "http://allrecipes.com/recipe/slow-cooker-chicken-taco-soup/";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_allrecipes_print_format() {
        $url       = "http://allrecipes.com/Recipe-Tools/Print/Recipe.aspx?recipeID=38109&origin=detail&servings=60&metric=false";
        $canonical = "http://allrecipes.com/Recipe/Pickled-Beets/Detail.aspx";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_allrecipes_kitchenview() {
        $url       = "http://allrecipes.com/recipe/kats-sausage-turnovers/kitchenview.aspx";
        $canonical = "http://allrecipes.com/recipe/kats-sausage-turnovers/detail.aspx";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_allrecipes_kitchenview_and_personalview() {
        $url       = "http://allrecipes.com/personalrecipe/64384170/chicken-and-veggies-with-rice/kitchenview.aspx";
        $canonical = "http://allrecipes.com/personalrecipe/64384170/chicken-and-veggies-with-rice/detail.aspx";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_foodnetwork_videos() {
        $url       = "http://www.foodnetwork.com/videos/oven-roasted-shrimp-and-garlic-0133122.html?ic1=tbla";
        $canonical = "http://www.foodnetwork.com/recipes/bobby-flay/oven-roasted-shrimp-with-toasted-garlic-and-red-chile-oil-recipe/index.html";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_yummyly_iframe() {
        $url       = "http://www.yummly.com/recipe/Roasted-Chicken-Tacos-Martha-Stewart-191942";
        $canonical = "http://www.yummly.com/recipe/external/Roasted-Chicken-Tacos-Martha-Stewart-191942";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_yummyly_recipe_external() {
        $url       = "http://www.yummly.com/recipe/external/Roasted-Chicken-Tacos-Martha-Stewart-191942";
        $canonical = "http://www.marthastewart.com/315717/roasted-chicken-tacos";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_foodnetwork_com_print_view() {
        $url       = "http://www.foodnetwork.com/recipes/giada-de-laurentiis/grilled-lamb-chops-recipe.print.html";
        $canonical = "http://www.foodnetwork.com/recipes/giada-de-laurentiis/grilled-lamb-chops-recipe.html";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_epicurious_com_print_view() {
        $url       = "http://www.epicurious.com/recipes/food/printerfriendly/celery-spiked-guacamole-with-chiles-51214860";
        $canonical = "http://www.epicurious.com/recipes/food/views/celery-spiked-guacamole-with-chiles-51214860";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_myrecipes_com_mobile_view() {
        $url       = "http://www.myrecipes.com/m/recipe/chicken-chickpea-tagine";
        $canonical = "http://www.myrecipes.com/recipe/chicken-chickpea-tagine";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_myrecipes_com_print_view() {
        $url       = "http://www.myrecipes.com/recipe/hummingbird-cake-0/print/";
        $canonical = "http://www.myrecipes.com/recipe/hummingbird-cake-0";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_myrecipes_com_quick_and_easy() {
        $url       = "http://www.myrecipes.com/quick-and-easy/dinner-tonight/dinner-tonight-june-2012?viewdate=6_4_2014&iid=edit-dt-060414";
        $canonical = "http://www.myrecipes.com/recipe/pan-seared-salmon-with-pineapple-jalapeno-relish";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_myrecipes_com_quick_and_easy_2() {
        $url       = "http://www.myrecipes.com/quick-and-easy/dinner-tonight/how-to-make-kung-pao-chicken";
        $canonical = "http://www.myrecipes.com/recipe/kung-pao-chicken";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_myrecipes_com_howto_videos() {
        $url       = "http://www.myrecipes.com/how-to/video/breakfast-enchiladas";
        $canonical = "http://www.myrecipes.com/recipe/breakfast-enchiladas";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }

    /**
     * @group network
     */
    public function test_food52_print_views() {
        $url       = "http://food52.com/recipes/print/17101";
        $canonical = "http://food52.com/recipes/17101";
        $html = FileUtil::downloadRecipeWithCache($url);
        $this->assertEquals($canonical, RecipeParser_Canonical::getCanonicalUrl($html, $url));
    }


}
