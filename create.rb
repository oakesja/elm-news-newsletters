require 'erb'
require 'json'


class Newsletter
  def initialize(articles_file)
    @home_page = 'http://elm-news.com'
    @icon_path = 'https://oakesja.github.io/elm-news/assets/images/newsletter-icon.png'
    @twitter_url = 'https://twitter.com/elmlangnews'
    @gitub_issues_url = 'https://github.com/oakesja/elm-news/issues'
    @submission_email = 'hello@elm-news.com'
    @articles = JSON.parse(File.read(articles_file))
    @now = Time.now.strftime('%F')
  end

  def build
    template = ERB.new(File.read('template.html.erb'))
    File.open('output.html', 'w') do |f|
      f.write(template.result(binding))
    end
  end
end

Newsletter.new(ARGV[0]).build
`xdg-open output.html`
