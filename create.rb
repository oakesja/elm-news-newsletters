require 'erb'
require 'json'
require 'cgi'


class Newsletter
  def initialize(articles_file)
    @home_page = 'http://elm-news.com'
    @icon_path = 'https://oakesja.github.io/elm-news/assets/images/newsletter-icon-dark.png'
    @twitter_url = 'https://twitter.com/elmlangnews'
    @gitub_issues_url = 'https://github.com/oakesja/elm-news/issues'
    @submission_email = 'hello@elm-news.com'
    @articles = articles_from(articles_file)
    @now = Time.now.strftime('%F')
  end

  def build
    template = ERB.new(File.read('template.html.erb'))
    File.open('output.html', 'w') do |f|
      f.write(template.result(binding))
    end
  end

  def articles_from(articles_file)
    articles = JSON.parse(File.read(articles_file))
    articles['articles'].each do |article|
      article['url'] = clean_url(article['url'])
    end
    articles
  end

  def clean_url(url)
    CGI::escape(url.chomp('/'))
  end
end

Newsletter.new(ARGV[0]).build
`xdg-open output.html`
